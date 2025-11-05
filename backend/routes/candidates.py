import os
import logging

from flask import Blueprint, request, jsonify, current_app, send_file
from werkzeug.utils import secure_filename
from models import db, Candidate
from datetime import datetime

from services.resume_parser import parse_resume
from services.ai_agent import generate_and_send_document_request


# Configure logging
logger = logging.getLogger(__name__)

candidates_bp = Blueprint('candidates', __name__)

# Allowed file extensions for resume upload
ALLOWED_RESUME_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename, allowed_extensions):
    """
    Check if the uploaded file has an allowed extension.

    Args:
        filename: Name of the file
        allowed_extensions: Set of allowed extensions

    Returns:
        Boolean indicating if file is allowed
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@candidates_bp.route('/upload', methods=['POST'])
def upload_resume():
    """
    POST /api/candidates/upload
    Accept and parse resume files (PDF/DOCX).

    Expected input:
        - file: Resume file (multipart/form-data)

    Returns:
        JSON response with extracted candidate data and confidence scores
    """
    # Check if file is present in request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    # Check if file is selected
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Validate file type
    if not allowed_file(file.filename, ALLOWED_RESUME_EXTENSIONS):
        return jsonify({
            'error': 'Invalid file type',
            'message': 'Only PDF and DOCX files are allowed'
        }), 400

    try:
        # Secure the filename
        filename = secure_filename(file.filename)

        # Save the file
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        logger.info(f"✅ File saved to: {file_path}")

        # Parse the resume using AI
        try:
            logger.info("Starting resume parsing...")
            # Extract structured data from resume
            extracted_data = parse_resume(file_path)

            logger.info("Creating candidate record in database...")

            # Create candidate with extracted data
            candidate = Candidate(
                name=extracted_data.get('name') or 'Unknown',
                email=extracted_data.get('email'),
                phone=extracted_data.get('phone'),
                company=extracted_data.get('company'),
                designation=extracted_data.get('designation'),
                skills=extracted_data.get('skills', []),
                experience_years=extracted_data.get('experience_years'),
                education=extracted_data.get('education', []),
                resume_filename=filename,
                resume_path=file_path,
                extraction_status='completed',
                confidence_scores=extracted_data.get('confidence_scores', {})
            )

            db.session.add(candidate)
            db.session.commit()

            logger.info(f"Candidate created successfully (ID: {candidate.id})")
            logger.info("="*60)
            logger.info("Resume upload and parsing completed successfully!")
            logger.info("="*60 + "\n")


            # Trigger agent asking for documents
            result = generate_and_send_document_request(candidate)
            if result.get('success'):
                logger.info(f"Document request sent to candidate: {candidate.email}")
            else:
                logger.warning(f"Document request failed: {result.get('error')}")

            return jsonify({
                'message': 'Resume uploaded and parsed successfully',
                'candidate': candidate.to_dict(include_details=True)
            }), 201

        except Exception as parsing_error:
            logger.error(f"Parsing error: {str(parsing_error)}")
            logger.warning("Saving candidate with 'failed' status...")

            # If parsing fails, still save the candidate with minimal info
            candidate = Candidate(
                name='Parsing Failed',
                resume_filename=filename,
                resume_path=file_path,
                extraction_status='failed'
            )

            db.session.add(candidate)
            db.session.commit()

            logger.info(f"Candidate saved with failed status (ID: {candidate.id})")
            logger.info("="*60 + "\n")

            return jsonify({
                'message': 'Resume uploaded but parsing failed',
                'error': str(parsing_error),
                'candidate': candidate.to_dict(include_details=True)
            }), 201

    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        db.session.rollback()
        # Clean up uploaded file if database operation fails
        if 'file_path' in locals() and os.path.exists(file_path):
            try:
                logger.info(f"Cleaning up file: {file_path}")
                os.remove(file_path)
            except:
                pass

        logger.info("="*60 + "\n")

        return jsonify({
            'error': 'Failed to process resume',
            'message': str(e)
        }), 500


@candidates_bp.route('', methods=['GET'])
def get_candidates():
    """
    GET /api/candidates
    List all candidates.

    Returns:
        JSON response with list of all candidates (summary view)
    """
    try:
        candidates = Candidate.query.order_by(Candidate.created_at.desc()).all()

        return jsonify({
            'candidates': [candidate.to_dict() for candidate in candidates]
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve candidates',
            'message': str(e)
        }), 500


@candidates_bp.route('/<candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    """
    GET /api/candidates/<id>
    Get detailed candidate profile with all extracted data.

    Args:
        candidate_id: UUID of the candidate

    Returns:
        JSON response with detailed candidate information including document URLs
    """
    try:
        candidate = Candidate.query.get(candidate_id)

        if not candidate:
            return jsonify({
                'error': 'Candidate not found',
                'message': f'No candidate found with ID {candidate_id}'
            }), 404

        candidate_data = candidate.to_dict(include_details=True)

        # Add document URLs if documents are uploaded
        if candidate.pan_document_path:
            candidate_data['pan_document_url'] = f'/candidates/{candidate_id}/documents/pan'

        if candidate.aadhaar_document_path:
            candidate_data['aadhaar_document_url'] = f'/candidates/{candidate_id}/documents/aadhaar'

        return jsonify(candidate_data), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve candidate',
            'message': str(e)
        }), 500


@candidates_bp.route('/<candidate_id>/request-documents', methods=['POST'])
def request_documents(candidate_id):
    """
    POST /api/candidates/<id>/request-documents
    AI agent generates personalized document request and sends email.

    This endpoint uses a LangGraph-based agent that:
    1. Analyzes the candidate profile
    2. Generates a personalized, culturally appropriate message
    3. Sends the message via email

    Args:
        candidate_id: UUID of the candidate

    Returns:
        JSON response with generated document request message and email status
    """
    try:
        candidate = Candidate.query.get(candidate_id)

        if not candidate:
            return jsonify({
                'error': 'Candidate not found',
                'message': f'No candidate found with ID {candidate_id}'
            }), 404

        # Validate that candidate has an email address
        if not candidate.email:
            return jsonify({
                'error': 'No email address',
                'message': 'Candidate does not have an email address on file'
            }), 400

        logger.info(f"Starting document request for candidate: {candidate.name}")

        # Use LangGraph agent to generate and send document request
        result = generate_and_send_document_request(candidate)

        if not result.get('success'):
            logger.error(f"Agent workflow failed: {result.get('error')}")
            return jsonify({
                'error': 'Failed to generate document request',
                'message': result.get('error', 'Unknown error occurred')
            }), 500

        # Update candidate record with the generated message
        candidate.document_request_sent = True
        candidate.document_request_text = result.get('message', '')
        candidate.document_request_sent_at = datetime.utcnow()

        db.session.commit()

        logger.info(f"Document request completed for: {candidate.name}")

        # Prepare response
        response_data = {
            'message': 'Document request generated and sent successfully',
            'request_text': result.get('message', ''),
            'request_sent_at': candidate.document_request_sent_at.isoformat(),
            'request_method': 'email',
            'email_sent': result.get('email_sent', False),
            'email_simulated': result.get('email_result', {}).get('simulated', False)
        }

        # Add error info if email failed but message was generated
        if not result.get('email_sent') and result.get('error'):
            response_data['email_error'] = result.get('error')
            response_data['message'] = 'Document request generated but email sending failed'

        return jsonify(response_data), 200

    except Exception as e:
        logger.error(f"Request documents error: {str(e)}")
        db.session.rollback()
        return jsonify({
            'error': 'Failed to process document request',
            'message': str(e)
        }), 500


@candidates_bp.route('/<candidate_id>/documents/<document_type>', methods=['GET'])
def get_document(candidate_id, document_type):
    """
    GET /api/candidates/<id>/documents/<pan|aadhaar>
    Serve uploaded document files for viewing/downloading.

    Args:
        candidate_id: UUID of the candidate
        document_type: Type of document ('pan' or 'aadhaar')

    Returns:
        The document file
    """
    try:
        candidate = Candidate.query.get(candidate_id)

        if not candidate:
            return jsonify({
                'error': 'Candidate not found',
                'message': f'No candidate found with ID {candidate_id}'
            }), 404

        # Get the appropriate document path
        if document_type == 'pan':
            document_path = candidate.pan_document_path
        elif document_type == 'aadhaar':
            document_path = candidate.aadhaar_document_path
        else:
            return jsonify({
                'error': 'Invalid document type',
                'message': 'Document type must be either "pan" or "aadhaar"'
            }), 400

        if not document_path or not os.path.exists(document_path):
            return jsonify({
                'error': 'Document not found',
                'message': f'{document_type.upper()} document has not been uploaded yet'
            }), 404

        # Serve the file
        return send_file(document_path, mimetype='application/octet-stream')

    except Exception as e:
        logger.error(f"Error serving document: {str(e)}")
        return jsonify({
            'error': 'Failed to retrieve document',
            'message': str(e)
        }), 500

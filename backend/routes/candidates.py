from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from models import db, Candidate
import os

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

        # TODO: Implement resume parsing logic
        # from services.resume_parser import parse_resume
        # extracted_data = parse_resume(file_path)

        # For now, create a placeholder candidate
        candidate = Candidate(
            name='Placeholder Name',
            email='placeholder@example.com',
            resume_filename=filename,
            resume_path=file_path,
            extraction_status='pending'
        )

        db.session.add(candidate)
        db.session.commit()

        return jsonify({
            'message': 'Resume uploaded successfully',
            'candidate': candidate.to_dict(include_details=True)
        }), 201

    except Exception as e:
        db.session.rollback()
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
        JSON response with detailed candidate information
    """
    try:
        candidate = Candidate.query.get(candidate_id)

        if not candidate:
            return jsonify({
                'error': 'Candidate not found',
                'message': f'No candidate found with ID {candidate_id}'
            }), 404

        return jsonify(candidate.to_dict(include_details=True)), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve candidate',
            'message': str(e)
        }), 500


@candidates_bp.route('/<candidate_id>/request-documents', methods=['POST'])
def request_documents(candidate_id):
    """
    POST /api/candidates/<id>/request-documents
    AI agent generates personalized document request.

    Args:
        candidate_id: UUID of the candidate

    Returns:
        JSON response with generated document request message
    """
    try:
        candidate = Candidate.query.get(candidate_id)

        if not candidate:
            return jsonify({
                'error': 'Candidate not found',
                'message': f'No candidate found with ID {candidate_id}'
            }), 404

        # TODO: Implement AI agent logic
        # from services.ai_agent import generate_document_request
        # request_text = generate_document_request(candidate)

        # Placeholder response
        request_text = f"Hi {candidate.name}, we need your PAN and Aadhaar documents for verification."

        # Update candidate record
        from datetime import datetime
        candidate.document_request_sent = True
        candidate.document_request_text = request_text
        candidate.document_request_sent_at = datetime.utcnow()

        db.session.commit()

        return jsonify({
            'message': 'Document request generated successfully',
            'request_text': request_text,
            'request_sent_at': candidate.document_request_sent_at.isoformat(),
            'request_method': 'email'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to generate document request',
            'message': str(e)
        }), 500

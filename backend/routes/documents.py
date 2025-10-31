from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from models import db, Candidate
import os
from datetime import datetime

documents_bp = Blueprint('documents', __name__)

# Allowed file extensions for document uploads
ALLOWED_DOCUMENT_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf'}


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


@documents_bp.route('/candidates/<candidate_id>/submit-documents', methods=['POST'])
def submit_documents(candidate_id):
    """
    POST /api/candidates/<id>/submit-documents
    Accept uploaded PAN/Aadhaar images.

    Expected input:
        - pan_image: File (JPG, PNG, or PDF)
        - aadhaar_image: File (JPG, PNG, or PDF)

    Args:
        candidate_id: UUID of the candidate

    Returns:
        JSON response confirming successful upload
    """
    try:
        # Verify candidate exists
        candidate = Candidate.query.get(candidate_id)

        if not candidate:
            return jsonify({
                'error': 'Candidate not found',
                'message': f'No candidate found with ID {candidate_id}'
            }), 404

        # Check if files are present
        if 'pan_image' not in request.files and 'aadhaar_image' not in request.files:
            return jsonify({
                'error': 'No files provided',
                'message': 'Please upload at least one document (PAN or Aadhaar)'
            }), 400

        pan_uploaded = False
        aadhaar_uploaded = False

        # Process PAN document
        if 'pan_image' in request.files:
            pan_file = request.files['pan_image']

            if pan_file.filename != '':
                # Validate file type
                if not allowed_file(pan_file.filename, ALLOWED_DOCUMENT_EXTENSIONS):
                    return jsonify({
                        'error': 'Invalid PAN file type',
                        'message': 'Only JPG, PNG, and PDF files are allowed for PAN'
                    }), 400

                # Secure and save the file
                filename = secure_filename(f"{candidate_id}_pan_{pan_file.filename}")
                file_path = os.path.join(current_app.config['DOCUMENTS_FOLDER'], filename)
                pan_file.save(file_path)

                # Update candidate record
                candidate.pan_document_path = file_path
                pan_uploaded = True

        # Process Aadhaar document
        if 'aadhaar_image' in request.files:
            aadhaar_file = request.files['aadhaar_image']

            if aadhaar_file.filename != '':
                # Validate file type
                if not allowed_file(aadhaar_file.filename, ALLOWED_DOCUMENT_EXTENSIONS):
                    return jsonify({
                        'error': 'Invalid Aadhaar file type',
                        'message': 'Only JPG, PNG, and PDF files are allowed for Aadhaar'
                    }), 400

                # Secure and save the file
                filename = secure_filename(f"{candidate_id}_aadhaar_{aadhaar_file.filename}")
                file_path = os.path.join(current_app.config['DOCUMENTS_FOLDER'], filename)
                aadhaar_file.save(file_path)

                # Update candidate record
                candidate.aadhaar_document_path = file_path
                aadhaar_uploaded = True

        # Update submission status
        if pan_uploaded or aadhaar_uploaded:
            candidate.documents_submitted = True
            candidate.documents_submitted_at = datetime.utcnow()
            db.session.commit()

            return jsonify({
                'message': 'Documents uploaded successfully',
                'pan_uploaded': pan_uploaded,
                'aadhaar_uploaded': aadhaar_uploaded,
                'uploaded_at': candidate.documents_submitted_at.isoformat()
            }), 200
        else:
            return jsonify({
                'error': 'No valid files uploaded',
                'message': 'Please select files to upload'
            }), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to upload documents',
            'message': str(e)
        }), 500

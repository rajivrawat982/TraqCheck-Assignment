from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, JSON
from datetime import datetime
import uuid

db = SQLAlchemy()


class Candidate(db.Model):
    """
    Candidate model to store parsed resume data and document tracking information.
    """
    __tablename__ = 'candidates'

    # Primary identification
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Basic information extracted from resume
    name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)
    company = Column(String)
    designation = Column(String)
    skills = Column(JSON)  # Array of strings
    experience_years = Column(Integer)
    education = Column(JSON)  # Array of strings

    # Resume metadata
    resume_filename = Column(String)
    resume_path = Column(String)
    extraction_status = Column(String, default='pending')  # 'pending', 'completed', 'failed'
    confidence_scores = Column(JSON)  # Dict of field: score

    # Document request tracking
    document_request_sent = Column(Boolean, default=False)
    document_request_text = Column(Text)
    document_request_sent_at = Column(DateTime)

    # Document submission tracking
    documents_submitted = Column(Boolean, default=False)
    pan_document_path = Column(String)
    aadhaar_document_path = Column(String)
    documents_submitted_at = Column(DateTime)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self, include_details=False):
        """
        Convert candidate object to dictionary for JSON responses.

        Args:
            include_details: If True, includes all fields. If False, returns summary view.

        Returns:
            Dictionary representation of the candidate
        """
        base_dict = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'company': self.company,
            'extraction_status': self.extraction_status,
            'documents_submitted': self.documents_submitted,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

        if include_details:
            base_dict.update({
                'phone': self.phone,
                'designation': self.designation,
                'skills': self.skills,
                'experience_years': self.experience_years,
                'education': self.education,
                'confidence_scores': self.confidence_scores,
                'document_request_sent': self.document_request_sent,
                'document_request_text': self.document_request_text,
                'document_request_sent_at': self.document_request_sent_at.isoformat() if self.document_request_sent_at else None,
                'pan_document_path': self.pan_document_path,
                'aadhaar_document_path': self.aadhaar_document_path,
                'documents_submitted_at': self.documents_submitted_at.isoformat() if self.documents_submitted_at else None,
                'updated_at': self.updated_at.isoformat() if self.updated_at else None
            })

        return base_dict

    def __repr__(self):
        return f'<Candidate {self.name} ({self.id})>'

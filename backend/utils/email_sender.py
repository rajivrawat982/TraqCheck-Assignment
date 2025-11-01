"""
Email Sending Utility

This module provides email sending functionality as a tool for the AI agent.
Supports both SMTP and simulated email sending for development/testing.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class EmailSender:
    """Email sender utility class"""

    def __init__(self):
        """Initialize email configuration from environment variables"""
        self.smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.from_email = os.getenv('FROM_EMAIL', self.smtp_username)
        self.simulate = os.getenv('SIMULATE_EMAIL', 'true').lower() == 'true'

    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Send an email to the specified recipient.

        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Plain text email body
            html_body: Optional HTML email body

        Returns:
            Dictionary with success status and message
        """
        if self.simulate:
            return self._simulate_email(to_email, subject, body)

        return self._send_smtp_email(to_email, subject, body, html_body)

    def _simulate_email(
        self,
        to_email: str,
        subject: str,
        body: str
    ) -> Dict[str, any]:
        """
        Simulate email sending for development/testing.

        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body

        Returns:
            Dictionary with success status and simulated message
        """
        logger.info("=" * 80)
        logger.info("SIMULATED EMAIL (Development Mode)")
        logger.info("=" * 80)
        logger.info(f"To: {to_email}")
        logger.info(f"Subject: {subject}")
        logger.info("-" * 80)
        logger.info(body)
        logger.info("=" * 80)

        return {
            'success': True,
            'message': 'Email simulated successfully (development mode)',
            'to': to_email,
            'subject': subject,
            'simulated': True
        }

    def _send_smtp_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Send actual email via SMTP.

        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Plain text email body
            html_body: Optional HTML email body

        Returns:
            Dictionary with success status and message
        """
        try:
            # Validate configuration
            if not self.smtp_username or not self.smtp_password:
                logger.warning("SMTP credentials not configured, falling back to simulation")
                return self._simulate_email(to_email, subject, body)

            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject

            # Attach plain text and HTML versions
            msg.attach(MIMEText(body, 'plain'))
            if html_body:
                msg.attach(MIMEText(html_body, 'html'))

            # Connect to SMTP server and send
            logger.info(f"Connecting to SMTP server: {self.smtp_host}:{self.smtp_port}")
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)

            logger.info(f"Email sent successfully to {to_email}")

            return {
                'success': True,
                'message': 'Email sent successfully',
                'to': to_email,
                'subject': subject,
                'simulated': False
            }

        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return {
                'success': False,
                'message': f'Failed to send email: {str(e)}',
                'to': to_email,
                'subject': subject,
                'error': str(e)
            }


# Global email sender instance
email_sender = EmailSender()


def send_document_request_email(
    candidate_name: str,
    candidate_email: str,
    message_body: str
) -> Dict[str, any]:
    """
    Tool function for LangGraph agent to send document request email.

    Args:
        candidate_name: Name of the candidate
        candidate_email: Email address of the candidate
        message_body: The personalized message body generated by the AI

    Returns:
        Dictionary with email sending result
    """
    subject = "Document Submission Request - TraqCheck"

    # Create HTML version for better presentation
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background-color: #4F46E5; color: white; padding: 20px; border-radius: 8px 8px 0 0;">
                    <h2 style="margin: 0;">TraqCheck - Document Request</h2>
                </div>
                <div style="background-color: #f9fafb; padding: 30px; border: 1px solid #e5e7eb; border-radius: 0 0 8px 8px;">
                    <div style="white-space: pre-wrap;">{message_body}</div>
                    <div style="margin-top: 30px; padding: 20px; background-color: #EEF2FF; border-left: 4px solid #4F46E5; border-radius: 4px;">
                        <p style="margin: 0; font-size: 14px;">
                            <strong>Note:</strong> Please ensure all documents are clear and legible.
                            Accepted formats: PDF, JPG, PNG
                        </p>
                    </div>
                </div>
                <div style="margin-top: 20px; text-align: center; color: #6B7280; font-size: 12px;">
                    <p>This is an automated message from TraqCheck HR System</p>
                </div>
            </div>
        </body>
    </html>
    """

    result = email_sender.send_email(
        to_email=candidate_email,
        subject=subject,
        body=message_body,
        html_body=html_body
    )

    return result

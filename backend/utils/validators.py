"""
Input Validation Helpers

This module contains utility functions for validating various types of input data.
"""

import re
from typing import Tuple


def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email address format.

    Args:
        email: Email address to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email:
        return False, "Email is required"

    email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    if not re.match(email_pattern, email):
        return False, "Invalid email format"

    return True, ""


def validate_phone(phone: str) -> Tuple[bool, str]:
    """
    Validate Indian phone number format.

    Args:
        phone: Phone number to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not phone:
        return False, "Phone number is required"

    # Remove spaces and hyphens
    phone_cleaned = re.sub(r'[\s-]', '', phone)

    # Check for valid Indian phone number patterns
    patterns = [
        r'^\+91\d{10}$',  # +911234567890
        r'^0\d{10}$',  # 01234567890
        r'^\d{10}$'  # 1234567890
    ]

    for pattern in patterns:
        if re.match(pattern, phone_cleaned):
            return True, ""

    return False, "Invalid phone number format. Expected 10-digit Indian phone number"


def validate_pan(pan: str) -> Tuple[bool, str]:
    """
    Validate PAN (Permanent Account Number) format.

    PAN format: 5 letters, 4 digits, 1 letter (e.g., ABCDE1234F)

    Args:
        pan: PAN number to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not pan:
        return False, "PAN is required"

    pan_pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
    if not re.match(pan_pattern, pan.upper()):
        return False, "Invalid PAN format. Expected format: ABCDE1234F"

    return True, ""


def validate_aadhaar(aadhaar: str) -> Tuple[bool, str]:
    """
    Validate Aadhaar number format.

    Aadhaar format: 12 digits (can include spaces)

    Args:
        aadhaar: Aadhaar number to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not aadhaar:
        return False, "Aadhaar is required"

    # Remove spaces
    aadhaar_cleaned = re.sub(r'\s', '', aadhaar)

    if not re.match(r'^\d{12}$', aadhaar_cleaned):
        return False, "Invalid Aadhaar format. Expected 12 digits"

    return True, ""


def validate_file_size(file_size: int, max_size: int = 10485760) -> Tuple[bool, str]:
    """
    Validate file size.

    Args:
        file_size: Size of the file in bytes
        max_size: Maximum allowed size in bytes (default: 10MB)

    Returns:
        Tuple of (is_valid, error_message)
    """
    if file_size > max_size:
        max_mb = max_size / (1024 * 1024)
        return False, f"File size exceeds maximum limit of {max_mb}MB"

    return True, ""


def validate_file_extension(filename: str, allowed_extensions: set) -> Tuple[bool, str]:
    """
    Validate file extension.

    Args:
        filename: Name of the file
        allowed_extensions: Set of allowed extensions (e.g., {'pdf', 'docx'})

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not filename or '.' not in filename:
        return False, "Invalid filename"

    extension = filename.rsplit('.', 1)[1].lower()

    if extension not in allowed_extensions:
        return False, f"Invalid file extension. Allowed: {', '.join(allowed_extensions)}"

    return True, ""

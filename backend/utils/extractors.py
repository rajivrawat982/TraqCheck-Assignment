"""
Data Extraction Helpers

This module contains utility functions for extracting specific data
from text using regex, AI, or other methods.
"""

import re
from typing import Optional, List


def extract_email(text: str) -> Optional[str]:
    """
    Extract email address from text.

    Args:
        text: Input text

    Returns:
        Email address if found, None otherwise
    """
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(email_pattern, text)
    return match.group(0) if match else None


def extract_phone(text: str) -> Optional[str]:
    """
    Extract Indian phone number from text.

    Args:
        text: Input text

    Returns:
        Phone number if found, None otherwise
    """
    # Indian phone number patterns
    patterns = [
        r'\+91[-\s]?\d{10}',  # +91-1234567890 or +91 1234567890
        r'0\d{10}',  # 01234567890
        r'\d{10}'  # 1234567890
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)

    return None


def extract_skills(text: str, skill_keywords: Optional[List[str]] = None) -> List[str]:
    """
    Extract skills from text based on keywords.

    Args:
        text: Input text
        skill_keywords: Optional list of skill keywords to search for

    Returns:
        List of identified skills

    TODO: Implement more sophisticated skill extraction using:
        - Predefined skill database
        - AI-based extraction
        - NER (Named Entity Recognition)
    """
    if skill_keywords is None:
        # Common technical skills (can be expanded)
        skill_keywords = [
            'Python', 'Java', 'JavaScript', 'TypeScript', 'React', 'Angular',
            'Vue', 'Node.js', 'Django', 'Flask', 'SQL', 'MongoDB', 'AWS',
            'Docker', 'Kubernetes', 'Git', 'Machine Learning', 'AI', 'Data Science'
        ]

    found_skills = []
    text_lower = text.lower()

    for skill in skill_keywords:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    return found_skills


def extract_experience_years(text: str) -> Optional[int]:
    """
    Extract years of experience from text.

    Args:
        text: Input text

    Returns:
        Number of years if found, None otherwise
    """
    # Patterns like "5 years", "5+ years", "5 yrs"
    patterns = [
        r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience)?',
        r'(?:experience|worked|working).*?(\d+)\+?\s*(?:years?|yrs?)'
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1))

    return None


def calculate_confidence_score(extracted_value: any, validation_checks: List[bool]) -> float:
    """
    Calculate confidence score for an extracted field.

    Args:
        extracted_value: The extracted value
        validation_checks: List of boolean validation checks

    Returns:
        Confidence score between 0 and 1
    """
    if extracted_value is None:
        return 0.0

    # Base confidence
    confidence = 0.5

    # Adjust based on validation checks
    if validation_checks:
        passed_checks = sum(validation_checks)
        confidence = passed_checks / len(validation_checks)

    return round(confidence, 2)

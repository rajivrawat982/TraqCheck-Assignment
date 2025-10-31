"""
AI Agent Service

This module handles the AI agent that generates personalized document
request messages using LangChain and LLMs.
"""

from typing import Dict, Any


def generate_document_request(candidate: Any) -> str:
    """
    Generate a personalized document request message for a candidate.

    This AI agent analyzes the candidate profile and generates a contextual,
    professional message requesting PAN and Aadhaar documents.

    Args:
        candidate: Candidate model instance with profile information

    Returns:
        Personalized document request message as string

    TODO: Implement the following:
        1. Set up LangChain with chosen LLM (OpenAI/Claude/OpenRouter)
        2. Create prompt template for document requests
        3. Generate personalized message based on candidate profile
        4. Ensure culturally appropriate language for Indian context
        5. Include candidate name and relevant details
    """
    # Placeholder implementation
    # This will be implemented in the next phase

    candidate_name = candidate.name if candidate.name else "there"
    company = candidate.company if candidate.company else "your organization"

    message = f"""Dear {candidate_name},

Thank you for your interest in joining {company}. To proceed with your application, we need to verify your identity documents.

Please submit the following documents at your earliest convenience:
1. PAN Card (Permanent Account Number)
2. Aadhaar Card

You can upload these documents through our secure portal. Both scanned copies and clear photographs are acceptable.

If you have any questions or concerns, please don't hesitate to reach out to our HR team.

Best regards,
HR Team"""

    return message


def setup_langchain_agent():
    """
    Set up LangChain agent with the chosen LLM.

    TODO: Implement LangChain setup with:
        - LLM configuration (OpenAI/Claude/OpenRouter)
        - Prompt templates
        - Agent tools and memory
    """
    pass
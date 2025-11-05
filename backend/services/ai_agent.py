"""
AI Agent Service using LangGraph

This module implements a LangGraph-based agent that:
1. Analyzes candidate profile
2. Generates personalized document request message
3. Sends email to the candidate
"""

import os
import logging
from typing import TypedDict, Optional

from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Import ChatAnthropic only when needed to avoid version conflicts
try:
    from langchain_anthropic import ChatAnthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    ChatAnthropic = None

logger = logging.getLogger(__name__)


# Define the state for our agent
class DocumentRequestState(TypedDict):
    """State object for the document request agent workflow"""
    candidate_id: str
    candidate_name: str
    candidate_email: str
    candidate_phone: Optional[str]
    candidate_company: Optional[str]
    candidate_designation: Optional[str]

    # Agent workflow state
    profile_analysis: str
    generated_message: str
    email_sent: bool
    email_result: dict
    error: Optional[str]


class DocumentRequestAgent:
    """LangGraph agent for generating and sending document requests"""

    def __init__(self):
        """Initialize the agent with LLM and workflow graph"""
        self.llm = self._setup_llm()
        self.graph = self._build_graph()

    def _setup_llm(self):
        """
        Set up the LLM based on available API keys.
        Priority: OpenAI -> Anthropic
        """
        openai_key = os.getenv('OPENAI_API_KEY')
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')

        if openai_key:
            logger.info("Using OpenAI GPT-4 for agent")
            return ChatOpenAI(
                model="gpt-4",
                temperature=0.7,
                api_key=openai_key
            )
        elif anthropic_key and ANTHROPIC_AVAILABLE:
            logger.info("Using Anthropic Claude for agent")
            return ChatAnthropic(
                model="claude-3-5-sonnet-20241022",
                temperature=0.7,
                api_key=anthropic_key
            )
        elif anthropic_key and not ANTHROPIC_AVAILABLE:
            logger.warning("Anthropic API key found but langchain-anthropic not properly installed")
            raise ValueError(
                "Anthropic API key is set but langchain-anthropic has compatibility issues. "
                "Please use OPENAI_API_KEY instead, or fix the package versions."
            )
        else:
            raise ValueError(
                "No AI API key found. Please set OPENAI_API_KEY or ANTHROPIC_API_KEY"
            )

    def _analyze_candidate_profile(self, state: DocumentRequestState) -> DocumentRequestState:
        """
        Node 1: Analyze the candidate profile to understand context.

        This helps the agent create more personalized messages.
        """
        logger.info(f"Analyzing profile for candidate: {state['candidate_name']}")

        try:
            # Create analysis prompt
            analysis_prompt = f"""
            Analyze the following candidate profile and provide a brief summary
            of what you know about them. This will be used to create a personalized
            document request message.

            Candidate Information:
            - Name: {state['candidate_name']}
            - Email: {state['candidate_email']}
            - Phone: {state.get('candidate_phone', 'Not provided')}
            - Company: {state.get('candidate_company', 'Not provided')}
            - Designation: {state.get('candidate_designation', 'Not provided')}

            Provide a brief, professional analysis (2-3 sentences) focusing on:
            1. Their professional background (if known)
            2. Appropriate tone for communication
            3. Any specific details to mention
            """

            messages = [
                SystemMessage(content="You are an HR assistant analyzing candidate profiles."),
                HumanMessage(content=analysis_prompt)
            ]

            response = self.llm.invoke(messages)
            analysis = response.content

            logger.info(f"Profile analysis complete")

            state['profile_analysis'] = analysis
            return state

        except Exception as e:
            logger.error(f"Error in profile analysis: {str(e)}")
            state['error'] = f"Profile analysis failed: {str(e)}"
            return state

    def _generate_document_request(self, state: DocumentRequestState) -> DocumentRequestState:
        """
        Node 2: Generate personalized document request message using AI.

        Uses the profile analysis to create a culturally appropriate,
        professional message requesting PAN and Aadhaar documents.
        """
        logger.info(f"Generating document request message")

        try:
            # Get frontend base URL from environment
            frontend_base_url = os.getenv('FRONTEND_BASE_URL', 'http://localhost:5173')
            document_upload_url = f"{frontend_base_url}/documents/{state['candidate_id']}"

            # Create message generation prompt
            generation_prompt = f"""
            Based on the following candidate profile and analysis, create a personalized,
            professional email message requesting identity documents.

            Candidate Information:
            - Name: {state['candidate_name']}
            - Email: {state['candidate_email']}
            - Current Company: {state.get('candidate_company', 'our organization')}
            - Designation: {state.get('candidate_designation', 'the position')}

            Profile Analysis:
            {state.get('profile_analysis', 'No analysis available')}

            Document Upload Link:
            {document_upload_url}

            Requirements for the message:
            1. Use a professional, warm tone suitable for Indian corporate context
            2. Request the following documents:
               - PAN Card (Permanent Account Number)
               - Aadhaar Card
            3. Explain these are needed for identity verification and compliance
            4. Mention that scanned copies or clear photos are acceptable
            5. Be culturally sensitive and professional
            6. Keep it concise (3-4 short paragraphs)
            7. Include a polite closing
            8. DO NOT include a subject line (only the body)
            9. DO NOT include sender name and organization
            10. Add Signature line as "Best regards, HR Team, TraqCheck"
            11. IMPORTANT: Include the document upload link in the email body.
                Make it prominent and easy to click.
                Use text like "You can upload your documents using this secure link: {document_upload_url}"

            Generate ONLY the email body text, without any subject line or metadata.
            """

            messages = [
                SystemMessage(content="""You are an expert HR communication specialist
                specializing in professional, culturally appropriate messages for Indian candidates.
                Generate clear, warm, and professional email content."""),
                HumanMessage(content=generation_prompt)
            ]

            response = self.llm.invoke(messages)
            generated_message = response.content.strip()

            logger.info(f"Message generated successfully")
            logger.info(f"Message preview: {generated_message[:100]}...")

            state['generated_message'] = generated_message
            return state

        except Exception as e:
            logger.error(f"Error in message generation: {str(e)}")
            state['error'] = f"Message generation failed: {str(e)}"
            return state

    def _send_email(self, state: DocumentRequestState) -> DocumentRequestState:
        """
        Node 3: Send the generated message via email.

        Uses the email_sender tool to deliver the message to the candidate.
        """
        logger.info(f"Sending email to: {state['candidate_email']}")

        try:
            from utils.email_sender import send_document_request_email

            result = send_document_request_email(
                candidate_name=state['candidate_name'],
                candidate_email=state['candidate_email'],
                message_body=state['generated_message']
            )

            state['email_sent'] = result.get('success', False)
            state['email_result'] = result

            if result.get('success'):
                print("Email sent successfully")
            else:
                print(f"Email sending failed: {result.get('message')}")

            return state

        except Exception as e:
            print(f"Error sending email: {str(e)}")
            state['error'] = f"Email sending failed: {str(e)}"
            state['email_sent'] = False
            state['email_result'] = {'success': False, 'error': str(e)}
            return state

    def _should_continue_to_email(self, state: DocumentRequestState) -> str:
        """
        Conditional edge: Decide whether to send email or end.

        Only send email if message generation was successful.
        """
        if state.get('error'):
            logger.warning(f"Error detected, skipping email: {state['error']}")
            return "end"

        if not state.get('generated_message'):
            logger.warning("No message generated, skipping email")
            return "end"

        if not state.get('candidate_email'):
            logger.warning("No email address, skipping email")
            state['error'] = "No email address provided"
            return "end"

        return "send_email"

    def _build_graph(self) -> StateGraph:
        """
        Build the LangGraph workflow for document request.

        Workflow:
        1. Analyze candidate profile
        2. Generate personalized message
        3. Conditionally send email (if no errors)
        4. End
        """
        # Create the graph
        workflow = StateGraph(DocumentRequestState)

        # Add nodes
        workflow.add_node("analyze_profile", self._analyze_candidate_profile)
        workflow.add_node("generate_message", self._generate_document_request)
        workflow.add_node("send_email", self._send_email)

        # Set entry point
        workflow.set_entry_point("analyze_profile")

        # Add edges
        workflow.add_edge("analyze_profile", "generate_message")

        # Conditional edge: only send email if generation was successful
        workflow.add_conditional_edges(
            "generate_message",
            self._should_continue_to_email,
            {
                "send_email": "send_email",
                "end": END
            }
        )

        # Final edge
        workflow.add_edge("send_email", END)

        # Compile the graph
        return workflow.compile()

    def run(self, candidate) -> dict:
        """
        Execute the document request workflow for a candidate.

        Args:
            candidate: Candidate model instance

        Returns:
            Dictionary with workflow results including generated message and email status
        """
        logger.info("="*80)
        logger.info(f"Starting document request workflow for: {candidate.name}")
        logger.info("="*80)

        # Initialize state from candidate
        initial_state: DocumentRequestState = {
            'candidate_id': candidate.id,
            'candidate_name': candidate.name or 'Candidate',
            'candidate_email': candidate.email or '',
            'candidate_phone': candidate.phone,
            'candidate_company': candidate.company,
            'candidate_designation': candidate.designation,
            'profile_analysis': '',
            'generated_message': '',
            'email_sent': False,
            'email_result': {},
            'error': None
        }

        try:
            # Run the graph
            final_state = self.graph.invoke(initial_state)

            print(final_state)

            return {
                'success': True,
                'message': final_state.get('generated_message', ''),
                'email_sent': final_state.get('email_sent', False),
                'email_result': final_state.get('email_result', {}),
                'error': final_state.get('error')
            }

        except Exception as e:
            logger.error(f"❌ Workflow execution failed: {str(e)}")
            logger.info("="*80)

            return {
                'success': False,
                'message': '',
                'email_sent': False,
                'email_result': {},
                'error': str(e)
            }


# Global agent instance (lazy initialization)
_agent_instance = None


def get_agent() -> DocumentRequestAgent:
    """Get or create the global agent instance"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = DocumentRequestAgent()
    return _agent_instance


def generate_and_send_document_request(candidate) -> dict:
    """
    Main function to generate and send document request.

    This function orchestrates the entire workflow using LangGraph:
    1. Analyzes candidate profile
    2. Generates personalized message using AI
    3. Sends email to candidate

    Args:
        candidate: Candidate model instance with profile information

    Returns:
        Dictionary with workflow results:
        {
            'success': bool,
            'message': str,  # Generated message text
            'email_sent': bool,
            'email_result': dict,
            'error': str or None
        }
    """
    agent = get_agent()
    return agent.run(candidate)

# LangGraph Agent for Document Request

## Overview

This document describes the LangGraph-based AI agent implementation for generating and sending personalized document request emails to candidates.

## Architecture

The agent workflow consists of three main nodes orchestrated by LangGraph:

```
┌──────────────────┐
│  Analyze Profile │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Generate Message │
└────────┬─────────┘
         │
         ▼
    ┌────────┐
    │ Check  │ ──No──► END
    └────┬───┘
         │ Yes
         ▼
┌──────────────────┐
│   Send Email     │
└────────┬─────────┘
         │
         ▼
        END
```

## Components

### 1. State Definition (`DocumentRequestState`)

The agent uses a typed state dictionary that tracks:
- **Candidate Information**: `candidate_id`, `candidate_name`, `candidate_email`, `candidate_phone`, `candidate_company`, `candidate_designation`
- **Workflow State**: `profile_analysis`, `generated_message`, `email_sent`, `email_result`, `error`

### 2. Nodes

#### Node 1: Analyze Profile
**File**: `backend/services/ai_agent.py:76`

**Purpose**: Analyzes the candidate's profile to understand context and determine the appropriate tone for communication.

**Process**:
1. Creates a prompt with candidate information
2. Uses LLM to generate a brief professional analysis (2-3 sentences)
3. Focuses on professional background, appropriate tone, and specific details to mention

**Output**: Updates `state['profile_analysis']`

#### Node 2: Generate Document Request
**File**: `backend/services/ai_agent.py:122`

**Purpose**: Generates a personalized, culturally appropriate document request message.

**Process**:
1. Uses the profile analysis from Node 1
2. Creates a detailed prompt for message generation
3. Ensures the message:
   - Uses professional, warm tone for Indian corporate context
   - Requests PAN and Aadhaar documents
   - Explains documents are needed for verification and compliance
   - Mentions acceptable formats (scanned copies or clear photos)
   - Is culturally sensitive and concise (4-6 paragraphs)

**Output**: Updates `state['generated_message']`

#### Node 3: Send Email
**File**: `backend/services/ai_agent.py:182`

**Purpose**: Sends the generated message via email using the email sender tool.

**Process**:
1. Calls `send_document_request_email()` from `utils/email_sender.py`
2. Passes candidate name, email, and generated message
3. Receives result with success status

**Output**: Updates `state['email_sent']` and `state['email_result']`

### 3. Conditional Edge

**Function**: `_should_continue_to_email()`
**File**: `backend/services/ai_agent.py:216`

**Purpose**: Determines whether to proceed with sending email or end the workflow.

**Conditions for sending email**:
- No errors in previous nodes
- Message was successfully generated
- Candidate has a valid email address

**Returns**:
- `"send_email"` - Proceed to email sending node
- `"end"` - Skip email and end workflow

### 4. Email Sender Tool

**File**: `backend/utils/email_sender.py`

**Features**:
- Supports both simulated and real SMTP email sending
- Development mode: Logs email to console (default)
- Production mode: Sends via SMTP server
- Creates HTML-formatted emails for better presentation
- Configurable via environment variables

**Configuration**:
```bash
# Development mode (default)
SIMULATE_EMAIL=true

# Production mode
SIMULATE_EMAIL=false
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password
FROM_EMAIL=your-email@gmail.com
```

## API Integration

### Endpoint
`POST /api/candidates/<candidate_id>/request-documents`

**File**: `backend/routes/candidates.py:201`

### Request Flow

1. **Validation**:
   - Checks if candidate exists
   - Validates candidate has email address

2. **Agent Execution**:
   - Calls `generate_and_send_document_request(candidate)`
   - Agent runs through all nodes sequentially

3. **Database Update**:
   - Sets `document_request_sent = True`
   - Stores `document_request_text` (generated message)
   - Records `document_request_sent_at` timestamp

4. **Response**:
   ```json
   {
     "message": "Document request generated and sent successfully",
     "request_text": "Generated message...",
     "request_sent_at": "2024-11-01T12:00:00",
     "request_method": "email",
     "email_sent": true,
     "email_simulated": true
   }
   ```

## LLM Configuration
The agent supports multiple LLM providers with automatic fallback:

### Priority Order:
1. **OpenAI GPT-4** (if `OPENAI_API_KEY` is set)
2. **Anthropic Claude** (if `ANTHROPIC_API_KEY` is set)


## Error Handling

The agent includes comprehensive error handling:

1. **Profile Analysis Errors**: Caught and stored in `state['error']`
2. **Message Generation Errors**: Workflow ends gracefully, error returned in response
3. **Email Sending Errors**: Email failure logged but workflow completes (message is still saved)
4. **Missing Email**: Validated before agent execution, returns 400 error
5. **Missing API Key**: Raises ValueError with clear message
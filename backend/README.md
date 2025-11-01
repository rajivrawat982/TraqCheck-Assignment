# TraqCheck Backend

Flask-based backend with AI-powered resume parsing and intelligent document collection.

## Tech Stack

- **Flask** - Web framework
- **SQLAlchemy** - ORM for database management
- **LangGraph & LangChain** - AI agent orchestration
- **OpenAI API** - GPT-4 for resume parsing and document requests
- **PyPDF2 & python-docx** - Document parsing
- **PostgreSQL** (production) / SQLite (development)

## Features

- **AI Resume Parser** - Extracts structured data from PDF/DOCX with confidence scores
- **LangGraph Agent** - Multi-step autonomous agent for document collection
- **Smart Extraction** - Identifies name, email, phone, company, designation, and skills
- **Document Management** - Secure PAN and Aadhaar storage
- **RESTful API** - Clean endpoints for frontend integration

## Project Structure

```
backend/
├── app.py                 # Main Flask application
├── models.py              # Database models (Candidate)
├── routes/
│   ├── candidates.py      # Candidate endpoints
│   └── documents.py       # Document handling endpoints
├── services/
│   ├── resume_parser.py   # PDF/DOCX parsing logic
│   ├── ai_agent.py        # AI agent for document requests
│   └── document_handler.py # Document upload/storage
├── utils/
│   ├── extractors.py      # Data extraction helpers
│   └── validators.py      # Input validation
├── uploads/               # Temporary resume storage
├── documents/             # Submitted documents storage
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables (create from .env.example)
```

## Quick Start

### Setup

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your OPENAI_API_KEY to .env

# Run application
python app.py
```

Server runs at `http://localhost:5000`

## API Endpoints

**Candidates**
- `POST /api/candidates/upload` - Upload and parse resume
- `GET /api/candidates` - List all candidates
- `GET /api/candidates/<id>` - Get candidate details
- `POST /api/candidates/<id>/request-documents` - Generate AI document request

**Documents**
- `POST /api/candidates/<id>/submit-documents` - Submit PAN/Aadhaar documents

## Database

SQLite for development (auto-created as `traqcheck.db`)
PostgreSQL for production (configure `DATABASE_URL` in `.env`)

## Deployment

Deployed on **Render** with PostgreSQL database and environment variables configured in dashboard.
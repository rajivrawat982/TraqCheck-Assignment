# TraqCheck Backend

Flask-based backend for the TraqCheck AI-powered resume parser and document collection system.

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

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
# At minimum, add one of the AI API keys (OpenAI, Anthropic, or OpenRouter)
```

### 5. Run the Application

```bash
# Development mode
python app.py

# Or using Flask CLI
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

## API Endpoints

### Candidates
- **POST** `/api/candidates/upload` - Upload and parse resume
- **GET** `/api/candidates` - List all candidates
- **GET** `/api/candidates/<id>` - Get candidate details
- **POST** `/api/candidates/<id>/request-documents` - Generate document request

### Documents
- **POST** `/api/candidates/<id>/submit-documents` - Submit PAN/Aadhaar documents

## Database

The application uses SQLite by default for development. The database file (`traqcheck.db`) will be created automatically when you first run the application.

For production, update the `DATABASE_URL` in `.env` to use PostgreSQL.
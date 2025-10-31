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

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
- **GET** `/api/health` - Verify API is running

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

## Next Steps

1. Implement resume parsing logic in `services/resume_parser.py`
2. Implement AI agent in `services/ai_agent.py`
3. Add proper error handling and validation
4. Write unit tests
5. Set up production database (PostgreSQL)

## Development Notes

- The `uploads/` and `documents/` directories are created automatically
- Database tables are created automatically on first run
- Use the `.gitignore` to prevent committing sensitive files
- All routes support CORS for frontend integration

## Testing

Test the API using curl or Postman:

```bash
# Health check
curl http://localhost:5000/api/health

# Upload resume (replace with actual file)
curl -X POST -F "file=@resume.pdf" http://localhost:5000/api/candidates/upload

# Get all candidates
curl http://localhost:5000/api/candidates
```
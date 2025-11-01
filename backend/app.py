import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from models import db

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Fix for Render/Railway PostgreSQL URL (they use postgres:// but SQLAlchemy needs postgresql://)
database_url = os.getenv('DATABASE_URL', 'sqlite:///traqcheck.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_FILE_SIZE', 10485760))  # 10MB default

# Upload folders
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['DOCUMENTS_FOLDER'] = os.getenv('DOCUMENTS_FOLDER', 'documents')

# Ensure upload directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DOCUMENTS_FOLDER'], exist_ok=True)

# Initialize extensions
CORS(app)
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()


# Import and register blueprints
from routes.candidates import candidates_bp
from routes.documents import documents_bp

app.register_blueprint(candidates_bp, url_prefix='/api/candidates')
app.register_blueprint(documents_bp, url_prefix='/api')


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Not found',
        'message': 'The requested resource was not found'
    }), 404


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file size exceeded errors."""
    return jsonify({
        'error': 'File too large',
        'message': 'The uploaded file exceeds the maximum allowed size (10MB)'
    }), 413


@app.errorhandler(500)
def internal_error(error):
    """Handle internal server errors."""
    db.session.rollback()
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred. Please try again later.'
    }), 500


if __name__ == '__main__':
    # Run the Flask development server
    app.run(
        debug=os.getenv('FLASK_ENV', 'development') == 'development',
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000))
    )

# TraqCheck Frontend

React-based frontend for AI-Powered Resume Parser & Document Collection System

## Tech Stack

- **React** with Vite
- **Tailwind CSS** for styling
- **TanStack Query** for data management
- **React Dropzone** for file uploads
- **Axios** for API communication

## Features

- **Resume Upload** - Drag-and-drop interface supporting PDF/DOCX formats
- **Candidate Dashboard** - Clean table view with all parsed candidates
- **Profile View** - Detailed information with AI confidence scores
- **AI Document Requests** - Generate personalized document collection messages
- **Document Upload** - Secure PAN and Aadhaar document submission
- **Responsive Design** - Mobile and desktop optimized

## Quick Start

### Setup

```bash
# Install dependencies
npm install

# Set environment variable
echo "VITE_API_BASE_URL=http://localhost:5000/api" > .env

# Start development server
npm run dev
```

App runs at `http://localhost:5173`

### Build

```bash
npm run build
```

Output in `dist/` folder ready for deployment.

## Project Structure

```
src/
├── components/         # Reusable UI components
├── pages/             # Main application pages
├── services/          # API integration
└── App.jsx            # Router configuration
```

## Deployment

Deployed on **Vercel** with automatic builds from main branch.
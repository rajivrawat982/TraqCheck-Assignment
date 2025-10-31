# TraqCheck Frontend

React frontend for TraqCheck - AI-Powered Resume Parser & Document Collection System

## Tech Stack

- **React** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **React Router** - Navigation
- **TanStack Query (React Query)** - Data fetching
- **Axios** - HTTP client
- **React Dropzone** - File uploads

## Project Structure

```
src/
├── components/
│   ├── ResumeUpload.jsx       # Drag-drop resume upload
│   ├── CandidateTable.jsx     # Dashboard table
│   ├── CandidateProfile.jsx   # Profile view with confidence scores
│   ├── DocumentSection.jsx    # Document request & upload
│   └── ProgressBar.jsx        # Upload progress indicator
├── pages/
│   ├── Dashboard.jsx          # Main dashboard page
│   └── CandidateDetail.jsx    # Individual candidate page
├── services/
│   └── api.js                 # API client
├── App.jsx                    # Router setup
└── main.jsx                   # Entry point
```

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

3. Update `.env` with your backend API URL:
```
VITE_API_BASE_URL=http://localhost:5000/api
```

### Development

Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Build

Build for production:
```bash
npm run build
```

Preview production build:
```bash
npm run preview
```

## Features

- **Resume Upload**: Drag-and-drop interface for PDF/DOCX files
- **Candidate Dashboard**: Table view of all candidates
- **Profile View**: Detailed candidate information with confidence scores
- **AI Document Requests**: Generate personalized document requests
- **Document Upload**: Accept PAN and Aadhaar documents
- **Responsive Design**: Works on desktop and mobile devices

## Environment Variables

- `VITE_API_BASE_URL` - Backend API base URL (default: `http://localhost:5000/api`)

## Deployment

### Vercel

1. Push code to GitHub
2. Import repository in Vercel
3. Set framework preset to **Vite**
4. Add environment variable: `VITE_API_BASE_URL`
5. Deploy

### Other Platforms

Build the project and serve the `dist` folder:
```bash
npm run build
```

The `dist` folder contains static files ready for deployment.

## API Integration

The frontend expects the backend API to be running at the URL specified in `VITE_API_BASE_URL`.

Key endpoints:
- `POST /candidates/upload` - Upload resume
- `GET /candidates` - List all candidates
- `GET /candidates/:id` - Get candidate details
- `POST /candidates/:id/request-documents` - Generate AI document request
- `POST /candidates/:id/submit-documents` - Submit documents

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

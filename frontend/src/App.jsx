import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import CandidateDetail from './pages/CandidateDetail';
import DocumentUpload from './pages/DocumentUpload';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/candidates/:id" element={<CandidateDetail />} />
        <Route path="/documents/:id" element={<DocumentUpload />} />
      </Routes>
    </Router>
  );
}

export default App;
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import CandidateProfile from '../components/CandidateProfile';
import DocumentSection from '../components/DocumentSection';
import { fetchCandidateById } from '../services/api';

const CandidateDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const { data: candidate, isLoading, refetch } = useQuery({
    queryKey: ['candidate', id],
    queryFn: () => fetchCandidateById(id),
  });

  const handleDocumentsSubmitted = () => {
    refetch();
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex justify-center items-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!candidate) {
    return (
      <div className="min-h-screen bg-gray-50 flex justify-center items-center">
        <div className="text-center">
          <p className="text-gray-500 text-lg mb-4">Candidate not found</p>
          <Link to="/" className="text-blue-600 hover:text-blue-800">
            Back to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center space-x-4">
            <button
              onClick={() => navigate('/')}
              className="text-gray-600 hover:text-gray-900"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M15 19l-7-7 7-7"
                />
              </svg>
            </button>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Candidate Details</h1>
              <p className="text-gray-600 text-sm mt-1">View and manage candidate information</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Profile */}
          <div className="lg:col-span-2">
            <CandidateProfile candidate={candidate} />
          </div>

          {/* Right Column - Documents */}
          <div className="lg:col-span-1">
            <DocumentSection
              candidateId={id}
              candidate={candidate}
              onDocumentsSubmitted={handleDocumentsSubmitted}
            />
          </div>
        </div>
      </main>
    </div>
  );
};

export default CandidateDetail;

import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import ResumeUpload from '../components/ResumeUpload';
import CandidateTable from '../components/CandidateTable';
import { fetchCandidates } from '../services/api';

const Dashboard = () => {
  const [showUpload, setShowUpload] = useState(true);

  const { data: candidates, isLoading, refetch } = useQuery({
    queryKey: ['candidates'],
    queryFn: fetchCandidates,
  });

  const handleUploadSuccess = (data) => {
    console.log('Upload successful:', data);
    setShowUpload(false);
    refetch();
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">TraqCheck</h1>
              <p className="text-gray-600 mt-1">AI-Powered Resume Parser & Document Collection</p>
            </div>
            {!showUpload && (
              <button
                onClick={() => setShowUpload(true)}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                Upload Resume
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Upload Section */}
        {showUpload && (
          <div className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Upload Resume</h2>
            <ResumeUpload onUploadSuccess={handleUploadSuccess} />
          </div>
        )}

        {/* Candidates Table */}
        <div>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-semibold text-gray-900">Candidates</h2>
            <button
              onClick={() => refetch()}
              className="px-4 py-2 text-sm bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
            >
              Refresh
            </button>
          </div>
          <CandidateTable candidates={candidates} loading={isLoading} />
        </div>
      </main>
    </div>
  );
};

export default Dashboard;

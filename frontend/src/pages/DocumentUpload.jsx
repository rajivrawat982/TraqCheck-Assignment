import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useDropzone } from 'react-dropzone';
import { fetchCandidateById } from '../services/api';

const DocumentUpload = () => {
  const { id } = useParams();
  const [candidate, setCandidate] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [panFile, setPanFile] = useState(null);
  const [aadhaarFile, setAadhaarFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(false);

  useEffect(() => {
    const loadCandidate = async () => {
      try {
        setLoading(true);
        const data = await fetchCandidateById(id);
        setCandidate(data);
        setUploadSuccess(data.documents_submitted);
      } catch (err) {
        setError('Failed to load candidate information');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadCandidate();
  }, [id]);

  const handleSubmitDocuments = async () => {
    if (!panFile || !aadhaarFile) {
      setError('Please upload both PAN and Aadhaar documents');
      return;
    }

    setUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append('pan_image', panFile);
    formData.append('aadhaar_image', aadhaarFile);

    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_BASE_URL}/candidates/${id}/submit-documents`,
        {
          method: 'POST',
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error('Failed to upload documents');
      }

      await response.json();
      setUploadSuccess(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  };

  const panDropzone = useDropzone({
    accept: {
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png'],
      'application/pdf': ['.pdf'],
    },
    maxFiles: 1,
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        setPanFile(acceptedFiles[0]);
      }
    },
  });

  const aadhaarDropzone = useDropzone({
    accept: {
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png'],
      'application/pdf': ['.pdf'],
    },
    maxFiles: 1,
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        setAadhaarFile(acceptedFiles[0]);
      }
    },
  });

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="mt-2 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (error && !candidate) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-lg p-6 max-w-md">
          <div className="text-red-600 text-center">
            <p className="text-lg font-semibold">Error</p>
            <p className="mt-2">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Document Upload</h1>

          {/* Candidate Information */}
          <div className="border-t border-gray-200 pt-4">
            <div className="space-y-2">
              <div>
                <span className="text-sm font-medium text-gray-500">Name:</span>
                <p className="text-lg text-gray-900">{candidate?.name || 'N/A'}</p>
              </div>
              <div>
                <span className="text-sm font-medium text-gray-500">Email:</span>
                <p className="text-lg text-gray-900">{candidate?.email || 'N/A'}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Upload Section */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          {uploadSuccess ? (
            <div className="text-center py-8">
              <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100 mb-4">
                <svg className="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Documents Submitted Successfully!</h3>
              <p className="text-gray-600">Your PAN and Aadhaar documents have been uploaded.</p>
            </div>
          ) : (
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Upload Required Documents</h3>
                <p className="text-sm text-gray-600 mb-6">
                  Please upload clear images or PDFs of your PAN Card and Aadhaar Card.
                </p>
              </div>

              {/* PAN Upload */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  PAN Card *
                </label>
                <div
                  {...panDropzone.getRootProps()}
                  className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
                    panDropzone.isDragActive
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-300 hover:border-gray-400 bg-gray-50'
                  }`}
                >
                  <input {...panDropzone.getInputProps()} />
                  {panFile ? (
                    <div className="flex items-center justify-center">
                      <svg className="h-5 w-5 text-green-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                      </svg>
                      <p className="text-sm text-green-600 font-medium">{panFile.name}</p>
                    </div>
                  ) : (
                    <div>
                      <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                        <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                      </svg>
                      <p className="mt-2 text-sm text-gray-600">
                        Drop PAN card image here or click to select
                      </p>
                      <p className="mt-1 text-xs text-gray-500">JPG, PNG or PDF (max 10MB)</p>
                    </div>
                  )}
                </div>
              </div>

              {/* Aadhaar Upload */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Aadhaar Card *
                </label>
                <div
                  {...aadhaarDropzone.getRootProps()}
                  className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
                    aadhaarDropzone.isDragActive
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-300 hover:border-gray-400 bg-gray-50'
                  }`}
                >
                  <input {...aadhaarDropzone.getInputProps()} />
                  {aadhaarFile ? (
                    <div className="flex items-center justify-center">
                      <svg className="h-5 w-5 text-green-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                      </svg>
                      <p className="text-sm text-green-600 font-medium">{aadhaarFile.name}</p>
                    </div>
                  ) : (
                    <div>
                      <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                        <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                      </svg>
                      <p className="mt-2 text-sm text-gray-600">
                        Drop Aadhaar card image here or click to select
                      </p>
                      <p className="mt-1 text-xs text-gray-500">JPG, PNG or PDF (max 10MB)</p>
                    </div>
                  )}
                </div>
              </div>

              {/* Error Message */}
              {error && (
                <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                  <p className="text-red-600 text-sm">Error: {error}</p>
                </div>
              )}

              {/* Submit Button */}
              <button
                onClick={handleSubmitDocuments}
                disabled={uploading || !panFile || !aadhaarFile}
                className="w-full px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {uploading ? 'Uploading...' : 'Submit Documents'}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DocumentUpload;
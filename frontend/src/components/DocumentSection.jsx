import { useState } from 'react';
import { useDropzone } from 'react-dropzone';

const DocumentSection = ({ candidateId, candidate, onDocumentsSubmitted }) => {
  const [panFile, setPanFile] = useState(null);
  const [aadhaarFile, setAadhaarFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [requestMessage, setRequestMessage] = useState(null);
  const [requestLoading, setRequestLoading] = useState(false);

  const handleRequestDocuments = async () => {
    setRequestLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_BASE_URL}/candidates/${candidateId}/request-documents`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      if (!response.ok) {
        throw new Error('Failed to generate document request');
      }

      const data = await response.json();
      setRequestMessage(data.request_text);
    } catch (err) {
      setError(err.message);
    } finally {
      setRequestLoading(false);
    }
  };

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
        `${import.meta.env.VITE_API_BASE_URL}/candidates/${candidateId}/submit-documents`,
        {
          method: 'POST',
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error('Failed to upload documents');
      }

      const data = await response.json();
      if (onDocumentsSubmitted) onDocumentsSubmitted(data);
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

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-xl font-bold text-gray-900 mb-6">Document Collection</h3>

      {/* Document Request Section */}
      <div className="mb-8">
        <div className="flex justify-between items-center mb-4">
          <h4 className="text-lg font-semibold text-gray-900">Request Documents</h4>
          {!candidate?.document_request_sent && (
            <button
              onClick={handleRequestDocuments}
              disabled={requestLoading}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {requestLoading ? 'Generating...' : 'Generate AI Request'}
            </button>
          )}
        </div>

        {candidate?.document_request_sent && (
          <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg">
            <p className="text-sm text-green-800">
              Document request sent on {new Date(candidate.document_request_sent_at).toLocaleString()}
            </p>
          </div>
        )}

        {requestMessage && (
          <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg">
            <p className="text-sm font-medium text-gray-700 mb-2">AI Generated Message:</p>
            <p className="text-gray-800 whitespace-pre-wrap">{requestMessage}</p>
          </div>
        )}
      </div>

      {/* Document Upload Section */}
      <div>
        <h4 className="text-lg font-semibold text-gray-900 mb-4">Upload Documents</h4>

        {candidate?.documents_submitted ? (
          <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
            <p className="text-green-800 font-medium">Documents already submitted</p>
            <p className="text-sm text-green-700 mt-1">
              Submitted on {new Date(candidate.documents_submitted_at).toLocaleString()}
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {/* PAN Upload */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                PAN Card
              </label>
              <div
                {...panDropzone.getRootProps()}
                className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors ${
                  panDropzone.isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'
                }`}
              >
                <input {...panDropzone.getInputProps()} />
                {panFile ? (
                  <p className="text-sm text-green-600">✓ {panFile.name}</p>
                ) : (
                  <p className="text-sm text-gray-500">
                    Drop PAN image here or click to select
                  </p>
                )}
              </div>
            </div>

            {/* Aadhaar Upload */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Aadhaar Card
              </label>
              <div
                {...aadhaarDropzone.getRootProps()}
                className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors ${
                  aadhaarDropzone.isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'
                }`}
              >
                <input {...aadhaarDropzone.getInputProps()} />
                {aadhaarFile ? (
                  <p className="text-sm text-green-600">✓ {aadhaarFile.name}</p>
                ) : (
                  <p className="text-sm text-gray-500">
                    Drop Aadhaar image here or click to select
                  </p>
                )}
              </div>
            </div>

            <button
              onClick={handleSubmitDocuments}
              disabled={uploading || !panFile || !aadhaarFile}
              className="w-full px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {uploading ? 'Uploading...' : 'Submit Documents'}
            </button>
          </div>
        )}

        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-600 text-sm">Error: {error}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default DocumentSection;

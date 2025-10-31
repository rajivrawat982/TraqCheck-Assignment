const CandidateProfile = ({ candidate }) => {
  if (!candidate) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Loading candidate information...</p>
      </div>
    );
  }

  const getConfidenceColor = (score) => {
    if (score >= 0.9) return 'text-green-600';
    if (score >= 0.7) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getConfidenceBarColor = (score) => {
    if (score >= 0.9) return 'bg-green-500';
    if (score >= 0.7) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const renderFieldWithConfidence = (label, value, confidenceScore) => {
    return (
      <div className="mb-4">
        <div className="flex justify-between items-center mb-1">
          <label className="text-sm font-medium text-gray-700">{label}</label>
          {confidenceScore !== undefined && (
            <span className={`text-xs font-medium ${getConfidenceColor(confidenceScore)}`}>
              {Math.round(confidenceScore * 100)}% confidence
            </span>
          )}
        </div>
        <p className="text-gray-900">{value || 'Not available'}</p>
        {confidenceScore !== undefined && (
          <div className="w-full bg-gray-200 rounded-full h-1.5 mt-1">
            <div
              className={`h-1.5 rounded-full ${getConfidenceBarColor(confidenceScore)}`}
              style={{ width: `${confidenceScore * 100}%` }}
            ></div>
          </div>
        )}
      </div>
    );
  };

  const confidenceScores = candidate.confidence_scores || {};

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="border-b pb-4 mb-6">
        <h2 className="text-2xl font-bold text-gray-900">{candidate.name}</h2>
        <p className="text-gray-600">{candidate.designation || 'Position not specified'}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Contact Information</h3>
          {renderFieldWithConfidence('Email', candidate.email, confidenceScores.email)}
          {renderFieldWithConfidence('Phone', candidate.phone, confidenceScores.phone)}
        </div>

        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Professional Details</h3>
          {renderFieldWithConfidence('Company', candidate.company, confidenceScores.company)}
          {renderFieldWithConfidence('Designation', candidate.designation, confidenceScores.designation)}
          {candidate.experience_years && (
            <div className="mb-4">
              <label className="text-sm font-medium text-gray-700">Experience</label>
              <p className="text-gray-900">{candidate.experience_years} years</p>
            </div>
          )}
        </div>
      </div>

      {candidate.skills && candidate.skills.length > 0 && (
        <div className="mt-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Skills</h3>
          <div className="flex flex-wrap gap-2">
            {candidate.skills.map((skill, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium"
              >
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}

      {candidate.education && candidate.education.length > 0 && (
        <div className="mt-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Education</h3>
          <ul className="list-disc list-inside space-y-1">
            {candidate.education.map((edu, index) => (
              <li key={index} className="text-gray-700">
                {edu}
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="mt-6 pt-6 border-t">
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-gray-600">Extraction Status:</span>
            <span className={`ml-2 font-medium ${
              candidate.extraction_status === 'completed' ? 'text-green-600' : 'text-yellow-600'
            }`}>
              {candidate.extraction_status}
            </span>
          </div>
          <div>
            <span className="text-gray-600">Created:</span>
            <span className="ml-2 text-gray-900">
              {new Date(candidate.created_at).toLocaleDateString()}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CandidateProfile;

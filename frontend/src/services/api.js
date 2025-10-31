import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Candidates API
export const fetchCandidates = async () => {
  try {
    const response = await api.get('/candidates');
    return response.data.candidates || response.data;
  } catch (error) {
    console.error('Error fetching candidates:', error);
    throw error;
  }
};

export const fetchCandidateById = async (id) => {
  try {
    const response = await api.get(`/candidates/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching candidate ${id}:`, error);
    throw error;
  }
};

export const uploadResume = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/candidates/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  } catch (error) {
    console.error('Error uploading resume:', error);
    throw error;
  }
};

export const requestDocuments = async (candidateId) => {
  try {
    const response = await api.post(`/candidates/${candidateId}/request-documents`);
    return response.data;
  } catch (error) {
    console.error('Error requesting documents:', error);
    throw error;
  }
};

export const submitDocuments = async (candidateId, panImage, aadhaarImage) => {
  try {
    const formData = new FormData();
    formData.append('pan_image', panImage);
    formData.append('aadhaar_image', aadhaarImage);

    const response = await api.post(`/candidates/${candidateId}/submit-documents`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  } catch (error) {
    console.error('Error submitting documents:', error);
    throw error;
  }
};

export default api;

import axios from 'axios';

const API_BASE_URL = '/api';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatWithAgent = async (sessionId, message, patientId) => {
  const response = await apiClient.post('/chat', {
    session_id: sessionId,
    message: message,
    patient_id: patientId
  });
  return response.data;
};

export const getDoctors = async () => {
  const response = await apiClient.get('/doctors');
  return response.data;
};

export const getAvailability = async (doctorId, dateStr) => {
  const response = await apiClient.get(`/doctors/${doctorId}/availability/${dateStr}`);
  return response.data;
};

export const setAvailability = async (data) => {
  const response = await apiClient.post('/doctors/availability', data);
  return response.data;
};

export const setStatus = async (doctorId, isActive) => {
  const response = await apiClient.post('/doctors/status', { doctor_id: doctorId, is_active: isActive });
  return response.data;
};

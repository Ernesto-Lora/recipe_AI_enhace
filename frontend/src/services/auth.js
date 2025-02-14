// src/services/auth.js
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/user';

export const login = async (email, password) => {
  const response = await axios.post(`${API_URL}/token/`, { email, password });
  return response.data.token; // Assuming the API returns a token
};

export const signIn = async (username, email, password) => {
  const response = await axios.post(`${API_URL}/create/`, { username, email, password });
  return response.data.token; // Assuming the API returns a token
};

export const fetchProtectedData = async () => {
  const token = getToken();
  const response = await axios.get(`${API_URL}/protected/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};
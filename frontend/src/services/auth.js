// src/services/auth.js
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/user';

export const login = async (email, password) => {
  console.log("HERE WE MAKE THE TOKEN REQUEST");
  const response = await axios.post(`${API_URL}/token/`, { email, password });
  
  return response.data.token; // Assuming the API returns a token
};

export const signUp = async (name, email, password) => {
  const response = await axios.post(`${API_URL}/create/`, { name, email, password });
  return response.data; // The response might not contain a token, so don't expect one here
};

export const fetchProtectedData = async () => {
  const token = getToken();
  const response = await axios.get(`${API_URL}/protected/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};
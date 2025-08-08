import axios from 'axios';
import * as SecureStore from 'expo-secure-store';

const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://10.0.2.2:8000';

const api = axios.create({ baseURL: `${API_BASE_URL}/api` });

api.interceptors.request.use(async (config) => {
  const token = await SecureStore.getItemAsync('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const login = async (email, password) => {
  const { data } = await api.post('/accounts/login/', { username: email, password });
  await SecureStore.setItemAsync('token', data.access);
  await SecureStore.setItemAsync('refresh', data.refresh);
  return data;
};

export const signup = (payload) => api.post('/accounts/signup/', payload);
export const getDevices = () => api.get('/devices/');
export const sendDeviceCommand = (id, command) => api.post(`/devices/${id}/command/`, { command });
export const getLatest = (deviceId) => api.get(`/measurements/latest/?device_id=${encodeURIComponent(deviceId)}`);
export const getHistory = (params) => api.get('/measurements/', { params });
export const getSettings = () => api.get('/measurements/settings/');
export const updateSettings = (payload) => api.put('/measurements/settings/', payload);

export default api;
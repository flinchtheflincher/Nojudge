import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001/api';

// Create axios instance
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor for error handling
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Token expired or invalid
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export default api;

// Auth API
export const authAPI = {
    signup: (email: string, password: string, personality_type: string) =>
        api.post('/auth/signup', { email, password, personality_type }),

    login: (email: string, password: string) =>
        api.post('/auth/login', { email, password }),

    getCurrentUser: () =>
        api.get('/auth/me'),
};

// Companion API
export const companionAPI = {
    getCompanion: () =>
        api.get('/companion/'),

    sendMessage: (message: string) =>
        api.post('/companion/message', { message }),

    getHistory: (limit = 50) =>
        api.get(`/companion/history?limit=${limit}`),

    getCurrentActivity: () =>
        api.get('/companion/activity'),

    triggerActivity: (activity: string) =>
        api.post('/companion/trigger-activity', { activity }),
};

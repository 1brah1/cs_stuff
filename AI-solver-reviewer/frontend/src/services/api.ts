import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export interface Document {
  id: number;
  filename: string;
  file_type: string;
  created_at: string;
  review_count: number;
}

export interface DocumentDetail extends Document {
  content: string;
  reviews: Review[];
}

export interface Review {
  id: number;
  document_id: number;
  review_text: string;
  status: string;
  created_at: string;
  document_filename?: string;
}

export const apiService = {
  // Auth
  async login(username: string = 'demo_user', password: string = 'demo') {
    const response = await api.post('/auth/login', null, {
      params: { username, password },
    });
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
    }
    return response.data;
  },

  // Documents
  async uploadDocument(file: File) {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post<Document>('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  async getDocuments(skip: number = 0, limit: number = 20) {
    const response = await api.get<Document[]>('/documents', {
      params: { skip, limit },
    });
    return response.data;
  },

  async getDocument(documentId: number) {
    const response = await api.get<DocumentDetail>(`/documents/${documentId}`);
    return response.data;
  },

  // Reviews
  async createReview(documentId: number) {
    const response = await api.post<Review>(`/reviews/${documentId}`);
    return response.data;
  },

  async getReviews(documentId: number) {
    const response = await api.get<Review[]>(`/reviews/${documentId}`);
    return response.data;
  },

  async getAllReviews(skip: number = 0, limit: number = 20) {
    const response = await api.get<Review[]>('/reviews', {
      params: { skip, limit },
    });
    return response.data;
  },
};

export default api;



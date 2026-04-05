import axios from 'axios';
import { getToken } from './auth';

// IMPORTANT: Use 10.0.2.2 for Android Emulators, or your local network IP (e.g., 192.168.x.x) for physical devices.
const API_BASE_URL = 'http://10.0.2.2:8000';

// --- Types mapping to your FastAPI models.schema ---
export interface MemoryResponse {
  message: string;
  memory_id: string;
  importance: number;
}

export interface QueryResponse {
  top_memories: string[];
  answer: string;
}

export interface DecayResponse {
  memory_id: string;
  strength: number;
  state: string;
}

// --- 1. Create the Axios Instance ---
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// --- 2. Setup the Auth Interceptor ---
// This runs automatically before EVERY request sent through `apiClient`
apiClient.interceptors.request.use(
  async (config) => {
    const token = await getToken();
    if (token) {
      // If a token exists in SecureStore, attach it to the Bearer header
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// --- 3. API Methods ---

/**
 * Maps to: POST /memory
 */
export const addMemory = async (text: string): Promise<MemoryResponse> => {
  // Notice how we don't pass headers here anymore? The interceptor handles it!
  const response = await apiClient.post<MemoryResponse>('/memory', { text });
  return response.data;
};

/**
 * Maps to: POST /query
 */
export const queryMemory = async (query: string): Promise<QueryResponse> => {
  const response = await apiClient.post<QueryResponse>('/query', { query });
  return response.data;
};

/**
 * Maps to: GET /memory/{memory_id}
 */
export const getMemoryById = async (memoryId: string): Promise<any> => {
  const response = await apiClient.get(`/memory/${memoryId}`);
  return response.data;
};

/**
 * Maps to: POST /memory/{memory_id}/decay
 */
export const triggerDecay = async (memoryId: string): Promise<DecayResponse> => {
  const response = await apiClient.post<DecayResponse>(`/memory/${memoryId}/decay`);
  return response.data;
};
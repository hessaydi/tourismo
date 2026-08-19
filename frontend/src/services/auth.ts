import { apiClient } from './api';
import { User, AuthResponse } from '@/types';

export const authService = {
  async register(username: string, email: string, fullName: string, password: string): Promise<User> {
    const response = await apiClient.post('/auth/register', {
      username,
      email,
      full_name: fullName,
      password,
    });
    return response.data;
  },

  async login(username: string, password: string): Promise<AuthResponse> {
    const response = await apiClient.post('/auth/login', {
      username,
      password,
    });
    const { access_token, refresh_token } = response.data;
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    return response.data;
  },

  async getCurrentUser(): Promise<User> {
    const response = await apiClient.get('/auth/me');
    return response.data;
  },

  async logout(): Promise<void> {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  async refreshToken(): Promise<string> {
    const response = await apiClient.post('/auth/refresh');
    const { access_token } = response.data;
    localStorage.setItem('access_token', access_token);
    return access_token;
  },

  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token');
  },

  getToken(): string | null {
    return localStorage.getItem('access_token');
  },
};

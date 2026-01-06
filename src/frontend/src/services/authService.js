import apiClient from '../api/client';
import { setToken, getToken, removeToken, setUser } from '../utils/storage';

export const login = async (username, password) => {
  try {
    const response = await apiClient.post('/auth/login', {
      username,
      password,
    });
    const { access_token } = response.data;
    setToken(access_token);
    
    // Store username for display purposes
    // Note: In a production app, you might want to decode the JWT or fetch user data
    setUser({ name: username });
    
    return { success: true, token: access_token };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Login failed',
    };
  }
};

export const register = async (username, password) => {
  try {
    const response = await apiClient.post('/auth/register', {
      username,
      password,
    });
    const user = response.data;
    setUser(user);
    
    // Auto-login after registration
    const loginResult = await login(username, password);
    return loginResult;
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Registration failed',
    };
  }
};

export const logout = () => {
  removeToken();
  setUser(null);
};

export const isAuthenticated = () => {
  return !!getToken();
};


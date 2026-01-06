import { createContext, useContext, useState, useEffect } from 'react';
import { getToken, getUser, setUser, removeUser } from '../utils/storage';
import * as authService from '../services/authService';

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUserState] = useState(getUser());
  const [token, setTokenState] = useState(getToken());
  const [isAuthenticated, setIsAuthenticated] = useState(!!getToken());

  const login = async (username, password) => {
    const result = await authService.login(username, password);
    if (result.success) {
      const userData = getUser();
      setUserState(userData);
      setTokenState(result.token);
      setIsAuthenticated(true);
    }
    return result;
  };

  const register = async (username, password) => {
    const result = await authService.register(username, password);
    if (result.success) {
      const userData = getUser();
      setUserState(userData);
      setTokenState(result.token);
      setIsAuthenticated(true);
    }
    return result;
  };

  const logout = () => {
    authService.logout();
    setUserState(null);
    setTokenState(null);
    setIsAuthenticated(false);
    removeUser();
  };

  useEffect(() => {
    const token = getToken();
    const userData = getUser();
    setIsAuthenticated(!!token);
    setUserState(userData);
    setTokenState(token);
  }, []);

  const value = {
    user,
    token,
    isAuthenticated,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};


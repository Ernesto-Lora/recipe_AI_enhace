// src/context/AuthContext.jsx
import React, { createContext, useState, useEffect } from 'react';
import { getToken, removeToken } from '../utils/auth';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isAuth, setIsAuth] = useState(!!getToken());

  const login = (token) => {
    setToken(token);
    setIsAuth(true);
  };

  const logout = () => {
    removeToken();
    setIsAuth(false);
  };

  return (
    <AuthContext.Provider value={{ isAuth, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
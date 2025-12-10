import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  // Mock user - always authenticated, no login required
  const [user] = useState({
    id: 'demo-user',
    email: 'demo@system.com',
    name: 'Demo User',
    role: 'Admin',
    department: null,
    is_active: true
  });

  const [loading] = useState(false);

  // Dummy functions to maintain compatibility
  const login = async () => {
    console.log('Login bypassed - direct access enabled');
    return user;
  };

  const register = async () => {
    console.log('Registration bypassed - direct access enabled');
  };

  const logout = () => {
    console.log('Logout called - but authentication is disabled');
  };

  return (
    <AuthContext.Provider value={{ user, login, register, logout, loading, isAuthenticated: true }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

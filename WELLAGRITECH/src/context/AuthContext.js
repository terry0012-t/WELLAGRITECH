import React, { createContext, useEffect, useState, useMemo } from 'react';
import * as SecureStore from 'expo-secure-store';
import { login as apiLogin } from '../services/api';

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      const token = await SecureStore.getItemAsync('token');
      setUser(token ? { token } : null);
      setLoading(false);
    })();
  }, []);

  const value = useMemo(() => ({
    user,
    loading,
    login: async (email, password) => {
      const data = await apiLogin(email, password);
      setUser({ token: data.access });
    },
    logout: async () => {
      await SecureStore.deleteItemAsync('token');
      await SecureStore.deleteItemAsync('refresh');
      setUser(null);
    },
  }), [user, loading]);

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}
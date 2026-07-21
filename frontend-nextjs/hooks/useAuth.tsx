"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';

const useAuth = () => {
  const [user, setUser] = useState(null);
  const router = useRouter();

  const login = async (email: string, password: string) => {
    try {
      const response = await axios.post('/api/v1/auth/login', { email, password });
      localStorage.setItem('token', response.data.token);
      setUser(response.data.user);
    } catch (error) {
      throw error;
    }
  };

  const register = async (email: string, password: string, companyName: string, role: string) => {
    try {
      await axios.post('/api/v1/auth/register', { email, password, companyName, role });
      router.push('/login');
    } catch (error) {
      throw error;
    }
  };

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      try {
        const response = await axios.get('/api/v1/auth/me');
        setUser(response.data.user);
      } catch (error) {
        localStorage.removeItem('token');
        setUser(null);
      }
    }
  }, []);

  return { user, login, register }; // Add more auth-related functions as needed
};

export default useAuth;

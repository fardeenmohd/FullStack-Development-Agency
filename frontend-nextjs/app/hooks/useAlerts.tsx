"use client";
import { useState, useEffect } from 'react';
import axios from 'axios';

const useAlerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const response = await axios.get('/api/alerts');
        setAlerts(response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchAlerts();
  }, []);

  const handleRequest = async (method, url, data = null) => {
    try {
      const response = await axios({ method, url, data });
      return response.data;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };

  const createAlert = async (alertData) => {
    const newAlert = await handleRequest('post', '/api/alerts', alertData);
    setAlerts([...alerts, newAlert]);
  };

  const updateAlert = async (id, updatedData) => {
    const updatedAlert = await handleRequest('put', `/api/alerts/${id}`, updatedData);
    setAlerts(alerts.map((alert) => (alert.id === id ? updatedAlert : alert)));
  };

  const deleteAlert = async (id) => {
    await handleRequest('delete', `/api/alerts/${id}`);
    setAlerts(alerts.filter((alert) => alert.id !== id));
  };

  return { alerts, loading, error, createAlert, updateAlert, deleteAlert };
};

export default useAlerts;

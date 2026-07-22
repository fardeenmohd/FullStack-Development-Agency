"use client";
import { useState, useEffect } from 'react';
import axios from 'axios';

const useAlerts = () => {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    fetchAlerts();
  }, []);

  const fetchAlerts = async () => {
    try {
      const response = await axios.get('/api/alerts');
      setAlerts(response.data);
    } catch (error) {
      console.error('Error fetching alerts:', error);
    }
  };

  const createOrUpdateAlert = async (alertData, isUpdate = false) => {
    try {
      const method = isUpdate ? 'put' : 'post';
      const url = isUpdate ? `/api/alerts/${alertData.id}` : '/api/alerts';
      const response = await axios[method](url, alertData);
      setAlerts((prevAlerts) =>
        isUpdate
          ? prevAlerts.map((alert) => (alert.id === alertData.id ? response.data : alert))
          : [...prevAlerts, response.data]
      );
    } catch (error) {
      console.error(isUpdate ? 'Error updating alert:' : 'Error creating alert:', error);
    }
  };

  const createAlert = async (alertData) => {
    await createOrUpdateAlert(alertData);
  };

  const updateAlert = async (id, updatedData) => {
    await createOrUpdateAlert({ ...updatedData, id }, true);
  };

  const deleteAlert = async (id) => {
    try {
      await axios.delete(`/api/alerts/${id}`);
      setAlerts((prevAlerts) => prevAlerts.filter((alert) => alert.id !== id));
    } catch (error) {
      console.error('Error deleting alert:', error);
    }
  };

  return { alerts, createAlert, updateAlert, deleteAlert };
};

export default useAlerts;

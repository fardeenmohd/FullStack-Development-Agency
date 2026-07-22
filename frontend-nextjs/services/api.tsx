import axios from 'axios';

const API_URL = 'https://api.example.com/lead-alerts';

const handleRequestError = (error: any, operation: string): never => {
  throw new Error(`${operation} failed: ${error.message}`);
};

export const createLeadAlert = async (alertData: any) => {
  try {
    const response = await axios.post(API_URL, alertData);
    return response.data;
  } catch (error) {
    handleRequestError(error, 'create lead alert');
  }
};

export const getLeadAlerts = async () => {
  try {
    const response = await axios.get(API_URL);
    return response.data;
  } catch (error) {
    handleRequestError(error, 'retrieve lead alerts');
  }
};

export const updateLeadAlert = async (alertId: string, alertData: any) => {
  try {
    const response = await axios.put(`${API_URL}/${alertId}`, alertData);
    return response.data;
  } catch (error) {
    handleRequestError(error, 'update lead alert');
  }
};

export const deleteLeadAlert = async (alertId: string) => {
  try {
    const response = await axios.delete(`${API_URL}/${alertId}`);
    return response.data;
  } catch (error) {
    handleRequestError(error, 'delete lead alert');
  }
};

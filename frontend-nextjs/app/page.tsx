"use client";
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AutomatedAlertsDashboard = () => {
  const [alerts, setAlerts] = useState([]);
  const [targetRegion, setTargetRegion] = useState('');
  const [productCategory, setProductCategory] = useState('');
  const [confidenceScoreThreshold, setConfidenceScoreThreshold] = useState(0);
  const [formError, setFormError] = useState('');

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const response = await axios.get('/api/v1/alerts');
        setAlerts(response.data);
      } catch (error) {
        console.error('Failed to fetch alerts:', error);
      }
    };

    fetchAlerts();
  }, []);

  const handleFormChange = (e) => {
    const { name, value, type } = e.target;
    if (type === 'number') {
      setConfidenceScoreThreshold(Number(value));
    } else {
      switch (name) {
        case 'targetRegion':
          setTargetRegion(value);
          break;
        case 'productCategory':
          setProductCategory(value);
          break;
        default:
          break;
      }
    }
  };

  const handleAlertChange = async () => {
    if (!targetRegion || !productCategory || confidenceScoreThreshold <= 0) {
      setFormError('Please fill in all fields.');
      return;
    }

    try {
      await axios.post('/api/v1/alerts', { targetRegion, productCategory, confidenceScoreThreshold });
      setAlerts([...alerts, { targetRegion, productCategory, confidenceScoreThreshold }]);
      resetForm();
      setFormError('');
    } catch (error) {
      console.error('Failed to update alert:', error);
      setFormError('Failed to add alert. Please try again.');
    }
  };

  const handleDeleteAlert = async (id) => {
    try {
      await axios.delete(`/api/v1/alerts/${id}`);
      setAlerts(alerts.filter(alert => alert.id !== id));
    } catch (error) {
      console.error('Failed to delete alert:', error);
      setFormError('Failed to delete alert. Please try again.');
    }
  };

  const resetForm = () => {
    setTargetRegion('');
    setProductCategory('');
    setConfidenceScoreThreshold(0);
  };

  return (
    <div className="flex h-screen bg-gray-900 text-white">
      <aside className="w-64 bg-gray-800 p-4">
        <h2 className="text-lg font-bold">Automated Alerts Dashboard</h2>
        <nav className="mt-4">
          <ul>
            {/* Add navigation items if needed */}
          </ul>
        </nav>
      </aside>
      <div className="flex flex-col flex-1">
        <header className="bg-gray-800 p-4 border-b border-gray-700">
          <div className="flex justify-between items-center">
            <img src="/logo.png" alt="Brand Logo" className="h-10" />
            <p>Welcome, Alerts Admin</p>
          </div>
        </header>
        <main className="flex flex-col p-4">
          <section className="bg-gray-700 p-4 rounded shadow mb-4">
            <h3>Timeline View</h3>
            <ul className="space-y-2">
              {alerts.map(alert => (
                <li key={alert.id} className="bg-gray-800 p-4 rounded shadow">
                  <div className="flex justify-between items-center">
                    <strong>{alert.targetRegion}</strong>: {alert.productCategory}, Confidence: {alert.confidenceScoreThreshold}
                  </div>
                  <button
                    onClick={() => handleDeleteAlert(alert.id)}
                    className="mt-2 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 focus:outline-none"
                  >
                    Delete
                  </button>
                </li>
              ))}
            </ul>
          </section>
          <section className="bg-gray-700 p-4 rounded shadow mb-4">
            <h3>Configure Alert</h3>
            <div className="mb-2">
              <label htmlFor="targetRegion" className="block text-sm font-medium">Target Region:</label>
              <input
                id="targetRegion"
                type="text"
                value={targetRegion}
                onChange={(e) => handleFormChange(e)}
                name="targetRegion"
                className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>
            <div className="mb-2">
              <label htmlFor="productCategory" className="block text-sm font-medium">Product Category:</label>
              <input
                id="productCategory"
                type="text"
                value={productCategory}
                onChange={(e) => handleFormChange(e)}
                name="productCategory"
                className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>
            <div className="mb-2">
              <label htmlFor="confidenceScoreThreshold" className="block text-sm font-medium">Confidence Score Threshold:</label>
              <input
                id="confidenceScoreThreshold"
                type="number"
                value={confidenceScoreThreshold}
                onChange={(e) => handleFormChange(e)}
                name="confidenceScoreThreshold"
                className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>
            {formError && (
              <p className="text-red-500 mt-2">{formError}</p>
            )}
            <button
              onClick={handleAlertChange}
              className="mt-2 px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 focus:outline-none"
            >
              Add Alert
            </button>
          </section>
        </main>
      </div>
    </div>
  );
};

export default AutomatedAlertsDashboard;

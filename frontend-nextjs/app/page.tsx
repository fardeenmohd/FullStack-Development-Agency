"use client";
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const NotificationsDashboard = () => {
  const [notifications, setNotifications] = useState([]);
  const [preferences, setPreferences] = useState({});
  const [newNotification, setNewNotification] = useState({ title: '', message: '' });
  const [showModal, setShowModal] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState(null);

  useEffect(() => {
    const fetchNotifications = async () => {
      try {
        const response = await axios.get('/api/v1/notifications');
        setNotifications(response.data);
      } catch (error) {
        console.error('Failed to fetch notifications:', error);
      }
    };

    const fetchPreferences = async () => {
      try {
        const response = await axios.get('/api/v1/preferences');
        setPreferences(response.data);
      } catch (error) {
        console.error('Failed to fetch preferences:', error);
      }
    };

    fetchNotifications();
    fetchPreferences();
  }, []);

  const handleAddNotification = async () => {
    try {
      await axios.post('/api/v1/notifications', newNotification);
      setNewNotification({ title: '', message: '' });
      fetchNotifications();
    } catch (error) {
      console.error('Failed to add notification:', error);
    }
  };

  const handleUpdatePreference = async (key, value) => {
    try {
      await axios.put('/api/v1/preferences', { [key]: value });
      setPreferences(prevPreferences => ({ ...prevPreferences, [key]: value }));
    } catch (error) {
      console.error('Failed to update preference:', error);
    }
  };

  const handleQuickExport = async () => {
    try {
      const response = await axios.get(`/api/v1/products/${selectedProduct}/leads`);
      setShowModal(true);
    } catch (error) {
      console.error('Failed to fetch leads:', error);
    }
  };

  const handleInitiateTransaction = async (leadId) => {
    try {
      await axios.post(`/api/v1/transactions`, { leadId });
      alert('Transaction initiated successfully!');
    } catch (error) {
      console.error('Failed to initiate transaction:', error);
    }
  };

  return (
    <div className="flex h-screen bg-gray-900 text-white">
      <aside className="w-64 bg-gray-800 p-4">
        <h2 className="text-lg font-bold">Notifications Dashboard</h2>
        <nav className="mt-4">
          <ul>
            <li className="mb-2"><a href="#" className="block px-3 py-2 rounded hover:bg-gray-700">Setup Notifications</a></li>
            <li className="mb-2"><a href="#" className="block px-3 py-2 rounded hover:bg-gray-700">View Active Notifications</a></li>
            <li><a href="#" className="block px-3 py-2 rounded hover:bg-gray-700">Manage Preferences</a></li>
          </ul>
        </nav>
      </aside>
      <div className="flex flex-col flex-1">
        <header className="bg-gray-800 p-4 border-b border-gray-700">
          <div className="flex justify-between items-center">
            <img src="/logo.png" alt="Brand Logo" className="h-10" />
            <p>Welcome, Notifications Admin</p>
          </div>
        </header>
        <main className="flex flex-col p-4">
          <section className="bg-gray-700 p-4 rounded shadow mb-4">
            <h3>Setup Notifications</h3>
            <input
              type="text"
              value={newNotification.title}
              onChange={(e) => setNewNotification({ ...newNotification, title: e.target.value })}
              placeholder="Title"
              className="w-full p-2 mt-2 border rounded"
            />
            <textarea
              value={newNotification.message}
              onChange={(e) => setNewNotification({ ...newNotification, message: e.target.value })}
              placeholder="Message"
              className="w-full p-2 mt-2 border rounded"
            />
            <button onClick={handleAddNotification} className="mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">Add Notification</button>
          </section>
          <section className="bg-gray-700 p-4 rounded shadow mb-4">
            <h3>View Active Notifications</h3>
            <ul>
              {notifications.map(notification => (
                <li key={notification.id} className="mb-2">{notification.title}: {notification.message}</li>
              ))}
            </ul>
          </section>
          <section className="bg-gray-700 p-4 rounded shadow">
            <h3>Manage Preferences</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label htmlFor="emailNotifications">Email Notifications:</label>
                <input
                  type="checkbox"
                  id="emailNotifications"
                  checked={preferences.emailNotifications}
                  onChange={(e) => handleUpdatePreference('emailNotifications', e.target.checked)}
                  className="ml-2"
                />
              </div>
              <div>
                <label htmlFor="smsNotifications">SMS Notifications:</label>
                <input
                  type="checkbox"
                  id="smsNotifications"
                  checked={preferences.smsNotifications}
                  onChange={(e) => handleUpdatePreference('smsNotifications', e.target.checked)}
                  className="ml-2"
                />
              </div>
            </div>
          </section>
        </main>
      </div>
    </div>
  );
};

export default NotificationsDashboard;

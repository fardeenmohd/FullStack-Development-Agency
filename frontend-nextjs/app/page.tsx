"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';

const Dashboard = () => {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [metrics, setMetrics] = useState({});
  const [products, setProducts] = useState([]);
  const [leads, setLeads] = useState([]);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await axios.get('/api/v1/auth/user');
        setUser(response.data);
      } catch (error) {
        console.error('Failed to fetch user:', error);
      }
    };

    const fetchMetrics = async () => {
      try {
        const response = await axios.get('/api/v1/dashboard/metrics');
        setMetrics(response.data);
      } catch (error) {
        console.error('Failed to fetch metrics:', error);
      }
    };

    const fetchProducts = async () => {
      try {
        const response = await axios.get('/api/v1/products');
        setProducts(response.data);
      } catch (error) {
        console.error('Failed to fetch products:', error);
      }
    };

    const fetchLeads = async () => {
      try {
        const response = await axios.get('/api/v1/leads');
        setLeads(response.data);
      } catch (error) {
        console.error('Failed to fetch leads:', error);
      }
    };

    fetchUser();
    fetchMetrics();
    fetchProducts();
    fetchLeads();
  }, []);

  const handleLogout = () => {
    router.push('/api/v1/auth/logout');
  };

  return (
    <div className="p-4">
      <h1>Dashboard</h1>
      {user && (
        <div>
          <p>Welcome, {user.company_name}</p>
          <button onClick={handleLogout}>Logout</button>
        </div>
      )}

      <h2>Metrics</h2>
      <pre>{JSON.stringify(metrics, null, 2)}</pre>

      <h2>Products</h2>
      <ul>
        {products.map(product => (
          <li key={product.id}>{product.name}</li>
        ))}
      </ul>

      <h2>Leads</h2>
      <ul>
        {leads.map(lead => (
          <li key={lead.id}>{lead.company_name} - Confidence: {lead.confidence_score}</li>
        ))}
      </ul>
    </div>
  );
};

export default Dashboard;

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
    <div className="flex h-screen bg-gray-900 text-white">
      <aside className="w-64 bg-gray-800 p-4">
        <h2 className="text-lg font-bold">Dashboard</h2>
        <nav className="mt-4">
          <ul>
            <li className="mb-2"><a href="#" className="block px-3 py-2 rounded hover:bg-gray-700">Overview</a></li>
            <li className="mb-2"><a href="#" className="block px-3 py-2 rounded hover:bg-gray-700">Products</a></li>
            <li className="mb-2"><a href="#" className="block px-3 py-2 rounded hover:bg-gray-700">Leads</a></li>
            <li><a href="#" onClick={handleLogout} className="block px-3 py-2 rounded hover:bg-gray-700">Logout</a></li>
          </ul>
        </nav>
      </aside>
      <div className="flex flex-col flex-1">
        <header className="bg-gray-800 p-4 border-b border-gray-700">
          <div className="flex justify-between items-center">
            <img src="/logo.png" alt="Brand Logo" className="h-10" />
            {user && (
              <div>
                <p>Welcome, {user.company_name}</p>
              </div>
            )}
          </div>
        </header>
        <main className="flex flex-col p-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-gray-700 p-4 rounded shadow">Metric 1</div>
            <div className="bg-gray-700 p-4 rounded shadow">Metric 2</div>
            <div className="bg-gray-700 p-4 rounded shadow">Metric 3</div>
            <div className="bg-gray-700 p-4 rounded shadow">Metric 4</div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default Dashboard;

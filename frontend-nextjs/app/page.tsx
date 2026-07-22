"use client";
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const LeadSegmentationDashboard = () => {
  const [leads, setLeads] = useState([]);
  const [filters, setFilters] = useState({
    country: '',
    industry: '',
    productInterest: ''
  });

  useEffect(() => {
    const fetchLeads = async () => {
      try {
        const response = await axios.get('/api/v1/leads');
        setLeads(response.data);
      } catch (error) {
        console.error('Failed to fetch leads:', error);
      }
    };

    fetchLeads();
  }, []);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prevFilters => ({
      ...prevFilters,
      [name]: value
    }));
  };

  const filteredLeads = leads.filter(lead => 
    (filters.country ? lead.country.toLowerCase().includes(filters.country.toLowerCase()) : true) &&
    (filters.industry ? lead.industry.toLowerCase().includes(filters.industry.toLowerCase()) : true) &&
    (filters.productInterest ? lead.productInterest.toLowerCase().includes(filters.productInterest.toLowerCase()) : true)
  );

  return (
    <div className="flex h-screen bg-gray-900 text-white">
      <aside className="w-64 bg-gray-800 p-4">
        <h2 className="text-lg font-bold">Lead Segmentation Dashboard</h2>
        <nav className="mt-4">
          <ul>
            {/* Add navigation items if needed */}
          </ul>
        </nav>
      </aside>
      <div className="flex flex-col flex-1">
        <header className="bg-gray-800 p-6 border-b border-gray-700">
          <div className="flex justify-between items-center">
            <img src="/logo.png" alt="Brand Logo" className="h-10" />
            <p>Welcome, Lead Admin</p>
          </div>
        </header>
        <main className="flex flex-col p-6">
          <section className="bg-gray-700 p-8 rounded-lg shadow mb-8 hover:bg-gray-800 transition-colors duration-200">
            <h3 className="text-xl font-semibold">Filter Leads</h3>
            <div className="mt-4 space-y-6">
              {Object.entries(filters).map(([filterName, filterValue]) => (
                <div key={filterName}>
                  <label htmlFor={filterName} className="block text-sm font-medium">{capitalize(filterName)}:</label>
                  <input
                    id={filterName}
                    type="text"
                    value={filterValue}
                    onChange={(e) => handleFilterChange(e)}
                    name={filterName}
                    className="mt-1 block w-full py-3 px-4 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                </div>
              ))}
            </div>
          </section>
          <section className="bg-gray-700 p-8 rounded-lg shadow mb-8 hover:bg-gray-800 transition-colors duration-200">
            <h3 className="text-xl font-semibold">Lead List</h3>
            <ul className="space-y-6 mt-4">
              {filteredLeads.map(lead => (
                <li key={lead.id} className="bg-gray-800 p-8 rounded-lg shadow hover:bg-gray-800 transition-colors duration-200">
                  <div className="flex justify-between items-center">
                    <strong>{lead.name}</strong>: {lead.country}, {lead.industry}, {lead.productInterest}
                  </div>
                </li>
              ))}
            </ul>
          </section>
          {/* Add sections for Historical Conversion Rates, Current Market Trends, and Actionable Insights */}
        </main>
      </div>
    </div>
  );
};

const capitalize = (str) => str.charAt(0).toUpperCase() + str.slice(1);

export default LeadSegmentationDashboard;

"use client";

import { useState, useEffect } from 'react';
import { useDashboardMetrics } from '../hooks/useDashboardMetrics';

export default function Dashboard({ metrics }: { metrics: any }) {
  const [activeLeads, setActiveLeads] = useState(0);
  const [totalTransactions, setTotalTransactions] = useState(0);
  const [averageContractValue, setAverageContractValue] = useState(0);

  useEffect(() => {
    if (metrics) {
      setActiveLeads(metrics.active_leads);
      setTotalTransactions(metrics.total_transactions);
      setAverageContractValue(metrics.average_contract_value);
    }
  }, [metrics]);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded shadow-md">
          <h2 className="text-xl font-bold">Active Leads</h2>
          <p>{activeLeads}</p>
        </div>
        <div className="bg-white p-4 rounded shadow-md">
          <h2 className="text-xl font-bold">Total Transactions</h2>
          <p>{totalTransactions}</p>
        </div>
        <div className="bg-white p-4 rounded shadow-md">
          <h2 className="text-xl font-bold">Average Contract Value</h2>
          <p>${averageContractValue.toFixed(2)}</p>
        </div>
      </div>
    </div>
  );
}

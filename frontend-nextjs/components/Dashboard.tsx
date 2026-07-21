import { useEffect, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

const fetchMetrics = async () => {
  const response = await axios.get('/api/v1/dashboard/metrics');
  return response.data;
};

export default function Dashboard() {
  const { data, isLoading, error } = useQuery('metrics', fetchMetrics);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <div className="mt-4">
        <h2 className="text-xl font-semibold">Trade Metrics</h2>
        <ul className="list-disc pl-5">
          {data.metrics.map((metric, index) => (
            <li key={index}>{metric.label}: {metric.value}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
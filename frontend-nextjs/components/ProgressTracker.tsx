import React from 'react';
import { Line } from 'react-chartjs-2';

const ProgressTracker = ({ data }) => {
  const chartData = {
    labels: data.map(item => item.date),
    datasets: [
      {
        label: 'Product Updates',
        data: data.map(item => item.productUpdates),
        backgroundColor: 'rgba(75,192,192,0.4)',
        borderColor: 'rgba(75,192,192,1)',
        borderWidth: 2,
      },
      {
        label: 'Collaboration Tasks',
        data: data.map(item => item.collaborationTasks),
        backgroundColor: 'rgba(255,99,132,0.4)',
        borderColor: 'rgba(255,99,132,1)',
        borderWidth: 2,
      },
    ],
  };

  return (
    <div>
      <h2>Progress Tracker</h2>
      <Line data={chartData} options={{ maintainAspectRatio: false }} />
    </div>
  );
};

export default ProgressTracker;

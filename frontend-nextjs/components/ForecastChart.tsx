import React from 'react';
import { Line } from 'react-chartjs-2';

const ForecastChart: React.FC = () => {
  // Define chart data with labels and datasets
  const data = {
    labels: ['January', 'February', 'March', 'April', 'May', 'June'],
    datasets: [
      {
        label: 'Historical Conversion Rates',
        data: [0.1, 0.15, 0.2, 0.25, 0.3, 0.35],
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
      {
        label: 'Predicted Trends',
        data: [0.2, 0.22, 0.24, 0.26, 0.28, 0.3],
        fill: false,
        borderColor: 'rgb(54, 162, 235)',
        tension: 0.1,
      },
    ],
  };

  // Define chart options
  const options = {
    responsive: true,
    plugins: {
      tooltip: {
        enabled: true,
        mode: 'index',
        intersect: false,
      },
      legend: {
        position: 'top' as const,
      },
    },
  };

  return <Line data={data} options={options} />;
};

export default ForecastChart;

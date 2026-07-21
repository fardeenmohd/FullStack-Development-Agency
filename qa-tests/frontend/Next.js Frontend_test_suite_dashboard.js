import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import Dashboard from '../components/Dashboard';

jest.mock('../api/dashboard', () => ({
  getMetrics: jest.fn()
}));

describe('Dashboard Component', () => {
  it('renders the dashboard with metrics', async () => {
    mockGetMetrics.mockResolvedValue({
      activeLeads: 10,
      totalTransactions: 50,
      averageContractValue: 20000
    });

    render(<Dashboard />);

    await screen.findByText(/active leads/i);
    expect(screen.getByText(/total transactions/i)).toBeInTheDocument();
    expect(screen.getByText(/average contract value/i)).toBeInTheDocument();
  });
});
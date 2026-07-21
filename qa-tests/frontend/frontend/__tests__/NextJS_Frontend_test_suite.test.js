import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Login from '../components/Login';
import Dashboard from '../components/Dashboard';
import LeadHunter from '../components/LeadHunter';
import ProductRegistration from '../components/ProductRegistration';

jest.mock('next/router', () => ({
  useRouter() {
    return {
      route: '/',
      pathname: '',
      query: '',
      asPath: '',
      push: jest.fn(),
    };
  },
}));

beforeEach(() => {
  global.fetch = jest.fn();
});

afterEach(() => {
  jest.resetAllMocks();
});

describe('Login Component', () => {
  test('renders login form and submits successfully', async () => {
    const mockPush = jest.fn();
    const useRouter = require('next/router').useRouter;
    useRouter.mockReturnValue({ push: mockPush });

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ token: 'mock-jwt-token' }),
    });

    render(<Login />);

    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'exporter@india.com' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'password123' } });
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith('/api/v1/auth/login', expect.any(Object));
      expect(mockPush).toHaveBeenCalledWith('/dashboard');
    });
  });
});

describe('Dashboard Component', () => {
  test('fetches and displays metrics and active leads', async () => {
    const mockMetrics = {
      activeLeads: 12,
      pendingTransactions: 3,
      totalExportValue: 150000,
    };

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockMetrics,
    });

    render(<Dashboard />);

    expect(screen.getByText(/loading/i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText(/12/)).toBeInTheDocument();
      expect(screen.getByText(/3/)).toBeInTheDocument();
      expect(screen.getByText(/\$150,000/)).toBeInTheDocument();
    });
  });
});

describe('LeadHunter Component', () => {
  test('triggers lead hunting and displays results', async () => {
    const mockLeads = [
      { id: '1', company_name: 'Oman Imports LLC', country: 'Oman', confidence_score: 92.5, status: 'NEW' }
    ];

    global.fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ status: 'success' }),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockLeads,
      });

    render(<LeadHunter />);

    const huntButton = screen.getByRole('button', { name: /hunt leads/i });
    fireEvent.click(huntButton);

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith('/api/v1/compute/hunt-leads', expect.any(Object));
      expect(screen.getByText('Oman Imports LLC')).toBeInTheDocument();
      expect(screen.getByText('92.5%')).toBeInTheDocument();
    });
  });
});

describe('ProductRegistration Component', () => {
  test('submits new product successfully', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: 'prod-123', name: 'Basmati Rice' }),
    });

    render(<ProductRegistration />);

    fireEvent.change(screen.getByLabelText(/product name/i), { target: { value: 'Basmati Rice' } });
    fireEvent.change(screen.getByLabelText(/hs code/i), { target: { value: '10063020' } });
    fireEvent.change(screen.getByLabelText(/description/i), { target: { value: 'Premium long-grain aromatic rice' } });
    fireEvent.change(screen.getByLabelText(/target region/i), { target: { value: 'OM' } });

    fireEvent.click(screen.getByRole('button', { name: /register product/i }));

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith('/api/v1/products', expect.objectContaining({
        method: 'POST'
      }));
      expect(screen.getByText(/product registered successfully/i)).toBeInTheDocument();
    });
  });
});
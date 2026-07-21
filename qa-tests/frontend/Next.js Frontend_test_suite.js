// Import necessary libraries and components
import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import App from '../App';
import Login from '../components/Login';
import Register from '../components/Register';
import Dashboard from '../components/Dashboard';
import ProductForm from '../components/ProductForm';
import LeadList from '../components/LeadList';
import TransactionForm from '../components/TransactionForm';

// Test suite for the Next.js Frontend
describe('Next.js Frontend', () => {
  // Test login functionality
  describe('Login Component', () => {
    test('renders login form with email and password fields', () => {
      render(<Login />);
      expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    });

    test('submits login form with valid credentials', async () => {
      render(<Login />);
      fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'test@example.com' } });
      fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'password123' } });
      fireEvent.click(screen.getByText(/login/i));
      expect(screen.getByText(/dashboard/i)).toBeInTheDocument();
    });
  });

  // Test register functionality
  describe('Register Component', () => {
    test('renders registration form with email, password, and company name fields', () => {
      render(<Register />);
      expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/company name/i)).toBeInTheDocument();
    });

    test('submits registration form with valid credentials', async () => {
      render(<Register />);
      fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'test@example.com' } });
      fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'password123' } });
      fireEvent.change(screen.getByLabelText(/company name/i), { target: { value: 'Test Company' } });
      fireEvent.click(screen.getByText(/register/i));
      expect(screen.getByText(/dashboard/i)).toBeInTheDocument();
    });
  });

  // Test dashboard functionality
  describe('Dashboard Component', () => {
    test('renders dashboard with metrics, leads, and transactions', () => {
      render(<Dashboard />);
      expect(screen.getByText(/metrics/i)).toBeInTheDocument();
      expect(screen.getByText(/leads/i)).toBeInTheDocument();
      expect(screen.getByText(/transactions/i)).toBeInTheDocument();
    });
  });

  // Test product form functionality
  describe('ProductForm Component', () => {
    test('renders product form with name, HS code, and target regions fields', () => {
      render(<ProductForm />);
      expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/HS code/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/target regions/i)).toBeInTheDocument();
    });

    test('submits product form with valid data', async () => {
      render(<ProductForm />);
      fireEvent.change(screen.getByLabelText(/name/i), { target: { value: 'Test Product' } });
      fireEvent.change(screen.getByLabelText(/HS code/i), { target: { value: '123456789012' } });
      fireEvent.change(screen.getByLabelText(/target regions/i), { target: { value: 'OM,CN,EU,AU' } });
      fireEvent.click(screen.getByText(/submit/i));
      expect(screen.getByText(/product registered successfully/i)).toBeInTheDocument();
    });
  });

  // Test lead list functionality
  describe('LeadList Component', () => {
    test('renders lead list with company name, country, and confidence score', () => {
      render(<LeadList />);
      expect(screen.getByText(/company name/i)).toBeInTheDocument();
      expect(screen.getByText(/country/i)).toBeInTheDocument();
      expect(screen.getByText(/confidence score/i)).toBeInTheDocument();
    });
  });

  // Test transaction form functionality
  describe('TransactionForm Component', () => {
    test('renders transaction form with lead ID, exporter ID, and contract value fields', () => {
      render(<TransactionForm />);
      expect(screen.getByLabelText(/lead ID/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/exporter ID/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/contract value/i)).toBeInTheDocument();
    });

    test('submits transaction form with valid data', async () => {
      render(<TransactionForm />);
      fireEvent.change(screen.getByLabelText(/lead ID/i), { target: { value: '12345678-1234-1234-1234-1234567890ab' } });
      fireEvent.change(screen.getByLabelText(/exporter ID/i), { target: { value: 'abcdef12-3456-7890-abcd-ef1234567890' } });
      fireEvent.change(screen.getByLabelText(/contract value/i), { target: { value: '1000.00' } });
      fireEvent.click(screen.getByText(/submit/i));
      expect(screen.getByText(/transaction initiated successfully/i)).toBeInTheDocument();
    });
  });
});
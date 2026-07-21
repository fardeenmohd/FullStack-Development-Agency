import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import Login from '../components/Login';

jest.mock('../api/auth', () => ({
  login: jest.fn()
}));

describe('Login Component', () => {
  it('renders the login form', () => {
    const { getByLabelText, getByText } = render(<Login />);
    expect(getByLabelText(/email/i)).toBeInTheDocument();
    expect(getByLabelText(/password/i)).toBeInTheDocument();
    expect(getByText(/login/i)).toBeInTheDocument();
  });

  it('submits the login form with valid credentials', async () => {
    const { getByLabelText, getByText } = render(<Login />);
    fireEvent.change(getByLabelText(/email/i), { target: { value: 'test@example.com' } });
    fireEvent.change(getByLabelText(/password/i), { target: { value: 'password123' } });
    fireEvent.click(getByText(/login/i));

    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith('test@example.com', 'password123');
    });
  });
});
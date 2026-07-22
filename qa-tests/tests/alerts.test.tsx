import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import AlertForm from './AlertForm';

describe('AlertForm', () => {
  it('renders form elements correctly', () => {
    render(<AlertForm />);
    expect(screen.getByLabelText(/alert name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/description/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /submit/i })).toBeInTheDocument();
  });

  it('handles form submission', async () => {
    const onSubmit = jest.fn();
    render(<AlertForm onSubmit={onSubmit} />);
    fireEvent.change(screen.getByLabelText(/alert name/i), { target: { value: 'Test Alert' } });
    fireEvent.change(screen.getByLabelText(/description/i), { target: { value: 'This is a test alert.' } });
    fireEvent.click(screen.getByRole('button', { name: /submit/i }));
    expect(onSubmit).toHaveBeenCalledWith({ name: 'Test Alert', description: 'This is a test alert.' });
  });
});

import axios from 'axios';
import { rest } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  rest.post('/api/alerts', (req, res, ctx) => {
    return res(ctx.status(201), ctx.json({ id: 1, name: 'Test Alert', description: 'This is a test alert.' }));
  }),
  rest.put('/api/alerts/1', (req, res, ctx) => {
    return res(ctx.status(200), ctx.json({ id: 1, name: 'Updated Test Alert', description: 'Updated description.' }));
  }),
  rest.delete('/api/alerts/1', (req, res, ctx) => {
    return res(ctx.status(204));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('Alert API Integration', () => {
  it('creates an alert', async () => {
    const response = await axios.post('/api/alerts', { name: 'Test Alert', description: 'This is a test alert.' });
    expect(response.status).toBe(201);
    expect(response.data).toEqual({ id: 1, name: 'Test Alert', description: 'This is a test alert.' });
  });

  it('updates an alert', async () => {
    const response = await axios.put('/api/alerts/1', { name: 'Updated Test Alert', description: 'Updated description.' });
    expect(response.status).toBe(200);
    expect(response.data).toEqual({ id: 1, name: 'Updated Test Alert', description: 'Updated description.' });
  });

  it('deletes an alert', async () => {
    const response = await axios.delete('/api/alerts/1');
    expect(response.status).toBe(204);
  });
});

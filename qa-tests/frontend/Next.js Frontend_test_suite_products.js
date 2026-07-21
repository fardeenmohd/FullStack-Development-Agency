import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import Products from '../components/Products';

jest.mock('../api/products', () => ({
  getProducts: jest.fn()
}));

describe('Products Component', () => {
  it('renders the products list', async () => {
    mockGetProducts.mockResolvedValue([
      { id: '1', name: 'Product A', hs_code: 'HS001' },
      { id: '2', name: 'Product B', hs_code: 'HS002' }
    ]);

    render(<Products />);

    await screen.findByText(/product a/i);
    expect(screen.getByText(/product b/i)).toBeInTheDocument();
  });

  it('adds a new product with valid data', async () => {
    const { getByLabelText, getByText } = render(<Products />);
    fireEvent.change(getByLabelText(/name/i), { target: { value: 'New Product' } });
    fireEvent.change(getByLabelText(/hs code/i), { target: { value: 'HS003' } });
    fireEvent.click(getByText(/add product/i));

    await waitFor(() => {
      expect(mockGetProducts).toHaveBeenCalled();
    });
  });
});
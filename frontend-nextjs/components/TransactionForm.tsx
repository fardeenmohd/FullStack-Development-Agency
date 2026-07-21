import React, { useState } from 'react';
import axios from 'axios';

const TransactionForm = () => {
  const [leadId, setLeadId] = useState('');
  const [contractValue, setContractValue] = useState(0);
  const [currency, setCurrency] = useState('USD');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post('/api/v1/transactions', {
        leadId,
        contractValue,
        currency,
      });
      alert('Transaction initiated successfully!');
      setLeadId('');
      setContractValue(0);
      setCurrency('USD');
    } catch (error) {
      console.error(error);
      alert('Failed to initiate transaction.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-4">
      <h2 className="text-xl font-bold">Initiate Transaction</h2>
      <div className="mt-4">
        <label htmlFor="leadId" className="block text-sm font-medium text-gray-700">
          Lead ID
        </label>
        <input
          type="text"
          id="leadId"
          value={leadId}
          onChange={(e) => setLeadId(e.target.value)}
          required
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm sm:text-sm"
        />
      </div>
      <div className="mt-4">
        <label htmlFor="contractValue" className="block text-sm font-medium text-gray-700">
          Contract Value
        </label>
        <input
          type="number"
          id="contractValue"
          value={contractValue}
          onChange={(e) => setContractValue(Number(e.target.value))}
          required
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm sm:text-sm"
        />
      </div>
      <div className="mt-4">
        <label htmlFor="currency" className="block text-sm font-medium text-gray-700">
          Currency
        </label>
        <input
          type="text"
          id="currency"
          value={currency}
          onChange={(e) => setCurrency(e.target.value)}
          required
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm sm:text-sm"
        />
      </div>
      <button type="submit" className="mt-4 bg-blue-500 text-white py-2 px-4 rounded">
        Initiate Transaction
      </button>
    </form>
  );
};

export default TransactionForm;
import React, { useState } from 'react';
import axios from 'axios';

const ProductForm = () => {
  const [name, setName] = useState('');
  const [hsCode, setHsCode] = useState('');
  const [description, setDescription] = useState('');
  const [targetRegions, setTargetRegions] = useState<string[]>([]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post('/api/v1/products', {
        name,
        hsCode,
        description,
        targetRegions,
      });
      alert('Product registered successfully!');
      setName('');
      setHsCode('');
      setDescription('');
      setTargetRegions([]);
    } catch (error) {
      console.error(error);
      alert('Failed to register product.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-4">
      <h2 className="text-xl font-bold">Register Product</h2>
      <div className="mt-4">
        <label htmlFor="name" className="block text-sm font-medium text-gray-700">
          Name
        </label>
        <input
          type="text"
          id="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm sm:text-sm"
        />
      </div>
      <div className="mt-4">
        <label htmlFor="hsCode" className="block text-sm font-medium text-gray-700">
          HS Code
        </label>
        <input
          type="text"
          id="hsCode"
          value={hsCode}
          onChange={(e) => setHsCode(e.target.value)}
          required
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm sm:text-sm"
        />
      </div>
      <div className="mt-4">
        <label htmlFor="description" className="block text-sm font-medium text-gray-700">
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          required
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm sm:text-sm"
        />
      </div>
      <div className="mt-4">
        <label htmlFor="targetRegions" className="block text-sm font-medium text-gray-700">
          Target Regions
        </label>
        <input
          type="text"
          id="targetRegions"
          value={targetRegions.join(',')}
          onChange={(e) => setTargetRegions(e.target.value.split(','))}
          required
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm sm:text-sm"
        />
      </div>
      <button type="submit" className="mt-4 bg-blue-500 text-white py-2 px-4 rounded">
        Register Product
      </button>
    </form>
  );
};

export default ProductForm;
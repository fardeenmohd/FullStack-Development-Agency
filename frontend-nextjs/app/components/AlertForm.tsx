"use client";
import React, { useState } from 'react';

interface AlertFormProps {
  onSubmit: (alertData: { name: string; category: string; region: string }) => void;
  initialAlert?: { name: string; category: string; region: string };
}

const AlertForm: React.FC<AlertFormProps> = ({ onSubmit, initialAlert }) => {
  const [formData, setFormData] = useState({
    name: initialAlert?.name || '',
    category: initialAlert?.category || '',
    region: initialAlert?.region || ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="name">Name:</label>
        <input
          type="text"
          id="name"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label htmlFor="category">Category:</label>
        <input
          type="text"
          id="category"
          name="category"
          value={formData.category}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label htmlFor="region">Region:</label>
        <input
          type="text"
          id="region"
          name="region"
          value={formData.region}
          onChange={handleChange}
          required
        />
      </div>
      <button type="submit">Submit</button>
    </form>
  );
};

export default AlertForm;

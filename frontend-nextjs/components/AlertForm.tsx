"use client";
import React, { useState } from 'react';

const AlertForm: React.FC = () => {
  const [formData, setFormData] = useState({
    targetRegions: '',
    productCategories: '',
    confidenceScoreThreshold: 0,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    if (name === 'confidence-score-threshold') {
      setFormData(prevState => ({
        ...prevState,
        [name]: Number(value),
      }));
    } else {
      setFormData(prevState => ({
        ...prevState,
        [name]: value,
      }));
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle form submission logic here
    console.log('Form Data:', formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="target-regions">Target Regions:</label>
        <input
          type="text"
          id="target-regions"
          name="targetRegions"
          value={formData.targetRegions}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label htmlFor="product-categories">Product Categories:</label>
        <input
          type="text"
          id="product-categories"
          name="productCategories"
          value={formData.productCategories}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label htmlFor="confidence-score-threshold">Confidence Score Threshold:</label>
        <input
          type="number"
          id="confidence-score-threshold"
          name="confidenceScoreThreshold"
          value={formData.confidenceScoreThreshold}
          onChange={handleChange}
          required
        />
      </div>
      <button type="submit">Create Alert</button>
    </form>
  );
};

export default AlertForm;

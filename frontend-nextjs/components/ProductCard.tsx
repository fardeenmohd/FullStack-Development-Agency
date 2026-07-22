import React from 'react';
import { Card, Button } from 'antd';

interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
}

const ProductCard: React.FC<{ product: Product }> = ({ product }) => {
  const handleCommentClick = () => {
    // Log the product name when the comment button is clicked
    console.log('Comment clicked for product:', product.name);
  };

  const handleTaskAssignmentClick = () => {
    // Log the product name when the task assignment button is clicked
    console.log('Task assigned for product:', product.name);
  };

  const handleProgressTrackClick = () => {
    // Log the product name when the progress track button is clicked
    console.log('Progress tracked for product:', product.name);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      {/* Display product details in a Card component */}
      <Card title={product.name} className="mb-4" style={{ width: '100%' }}>
        <p className="text-gray-700 mb-3">{product.description}</p>
        <p className="text-xl font-semibold text-gray-900">Price: ${product.price}</p>
      </Card>
      {/* Buttons to handle different actions */}
      <Button type="primary" onClick={handleCommentClick} className="hover:bg-blue-800 transition-colors duration-200 rounded-lg mr-4">
        Comment
      </Button>
      <Button type="primary" onClick={handleTaskAssignmentClick} className="hover:bg-blue-800 transition-colors duration-200 rounded-lg mr-4">
        Assign Task
      </Button>
      <Button type="primary" onClick={handleProgressTrackClick} className="hover:bg-blue-800 transition-colors duration-200 rounded-lg">
        Track Progress
      </Button>
    </div>
  );
};

export default ProductCard;

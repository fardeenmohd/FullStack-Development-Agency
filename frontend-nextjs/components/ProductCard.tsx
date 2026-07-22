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

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      {/* Display product details in a Card component */}
      <Card title={product.name} className="mb-4" style={{ width: '100%' }}>
        <p className="text-gray-700 mb-3">{product.description}</p>
        <p className="text-xl font-semibold text-gray-900">Price: ${product.price}</p>
      </Card>
      {/* Button to handle comment click */}
      <Button type="primary" onClick={handleCommentClick} className="hover:bg-blue-800 transition-colors duration-200 rounded-lg">
        Comment
      </Button>
    </div>
  );
};

export default ProductCard;

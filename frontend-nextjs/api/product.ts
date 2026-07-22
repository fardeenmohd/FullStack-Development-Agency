import express from 'express';
import jwt from 'jsonwebtoken';
import { Product } from '../models/product';

const router = express.Router();

interface CollaborateRequest {
  productId: string;
  userId: string;
}

router.post('/api/v1/products/collaborate', (req, res) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) {
    return res.status(401).json({ message: 'Unauthorized' });
  }

  jwt.verify(token, process.env.JWT_SECRET!, (err, decoded) => {
    if (err) {
      return res.status(401).json({ message: 'Unauthorized' });
    }

    const { productId, userId } = req.body as CollaborateRequest;

    handleProductCollaboration(productId, userId)
      .then((message) => res.json({ message }))
      .catch((error) => res.status(500).json({ message: 'Error sharing product', error }));
  });
});

const handleProductCollaboration = async (productId: string, userId: string): Promise<string> => {
  const product = await Product.findById(productId);
  if (!product) {
    throw new Error('Product not found');
  }

  product.collaborators.push(userId);
  await product.save();
  return 'Product shared successfully';
};

export default router;

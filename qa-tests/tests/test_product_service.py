import unittest
from unittest.mock import patch
from services.product_service import ProductService

class TestProductService(unittest.TestCase):

    @patch('services.product_service.send_notification')
    def test_update_product_notifies_users(self, mock_send_notification):
        # Arrange
        product_service = ProductService()
        product_id = 123
        updated_product = {'name': 'Updated Product', 'price': 9.99}
        
        # Act
        product_service.update_product(product_id, updated_product)
        
        # Assert
        mock_send_notification.assert_called_once_with(product_id)

if __name__ == '__main__':
    unittest.main()

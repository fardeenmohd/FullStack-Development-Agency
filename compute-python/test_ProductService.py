import unittest
from fastapi.testclient import TestClient
from services.NotificationService import NotificationService
from repositories.NotificationRepository import NotificationRepository
from main import app, product_service

class TestProductService(unittest.IsolatedAsyncioTestCase):
    async def setUp(self):
        self.notification_service = NotificationService()
        self.notification_repository = NotificationRepository()
        self.product_service = ProductService(self.notification_service, self.notification_repository)
        self.client = TestClient(app)

    async def test_update_product(self):
        new_details = {'price': 9.99}
        updated_product = await self.product_service.update_product(123, new_details)
        self.assertIsNotNone(updated_product)
        self.assertEqual(updated_product['price'], 9.99)

    async def test_connect_and_disconnect_websocket(self):
        websocket = TestClient(app).websocket_connect("/ws")
        await product_service.connect(websocket)
        self.assertIn(websocket, product_service.websocket_clients)
        await product_service.disconnect(websocket)
        self.assertNotIn(websocket, product_service.websocket_clients)

    async def test_trigger_notifications(self):
        updated_product = {'name': 'Test Product', 'price': 9.99}
        await self.product_service.trigger_notifications(updated_product)
        # Assuming NotificationService and NotificationRepository have been mocked
        # to verify that send_notification and save_notification are called

    async def test_send_real_time_updates(self):
        updated_product = {'name': 'Test Product', 'price': 9.99}
        websocket = TestClient(app).websocket_connect("/ws")
        await product_service.connect(websocket)
        await self.product_service.send_real_time_updates(updated_product)
        # Assuming the WebSocket has been mocked to verify that send_json is called

if __name__ == '__main__':
    unittest.main()

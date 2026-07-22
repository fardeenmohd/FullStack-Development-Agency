from services.NotificationService import NotificationService
from repositories.NotificationRepository import NotificationRepository
from fastapi import WebSocket, FastAPI

app = FastAPI()

class ProductService:
    def __init__(self, notification_service: NotificationService, notification_repository: NotificationRepository):
        self.notification_service = notification_service
        self.notification_repository = notification_repository
        self.websocket_clients = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.websocket_clients.add(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.websocket_clients.remove(websocket)

    async def update_product(self, product_id, new_details):
        updated_product = self.update_product_in_database(product_id, new_details)
        await self.trigger_notifications(updated_product)
        await self.send_real_time_updates(updated_product)
        return updated_product

    def update_product_in_database(self, product_id, new_details):
        # Placeholder for actual database update logic
        pass

    async def trigger_notifications(self, updated_product):
        notification_message = f"Product {updated_product['name']} has been updated."
        self.notification_service.send_notification(notification_message)
        self.notification_repository.save_notification(notification_message)

    async def send_real_time_updates(self, updated_product):
        for client in self.websocket_clients:
            await client.send_json(updated_product)

product_service = ProductService(NotificationService(), NotificationRepository())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await product_service.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming messages if needed
    finally:
        await product_service.disconnect(websocket)

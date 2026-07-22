from services.NotificationService import NotificationService
from repositories.NotificationRepository import NotificationRepository

class ProductService:
    def __init__(self, notification_service: NotificationService, notification_repository: NotificationRepository):
        self.notification_service = notification_service
        self.notification_repository = notification_repository

    def update_product(self, product_id, new_details):
        # Logic to update the product in the database
        updated_product = self.update_product_in_database(product_id, new_details)

        # Trigger notifications for the updated product
        self.trigger_notifications(updated_product)

        return updated_product

    def update_product_in_database(self, product_id, new_details):
        # Placeholder for actual database update logic
        pass

    def trigger_notifications(self, updated_product):
        notification_message = f"Product {updated_product['name']} has been updated."
        self.notification_service.send_notification(notification_message)
        self.notification_repository.save_notification(notification_message)

# Example usage:
# notification_service = NotificationService()
# notification_repository = NotificationRepository()
# product_service = ProductService(notification_service, notification_repository)
# product_service.update_product(123, {'price': 9.99})
```

This code snippet modifies the `ProductService` class to include logic for triggering notifications when product listings are updated. It integrates with the `NotificationService` and `NotificationRepository` to send and save notification messages.

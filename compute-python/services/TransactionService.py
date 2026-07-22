from services.NotificationService import NotificationService
from repositories.NotificationRepository import NotificationRepository

class TransactionService:
    def __init__(self, notification_repository: NotificationRepository):
        self.notification_service = NotificationService(notification_repository)

    def update_transaction_status(self, transaction_id, new_status):
        # Logic to update the transaction status in the database
        pass

    def trigger_notification_on_status_change(self, transaction_id, old_status, new_status):
        if old_status != new_status:
            notification_message = self._create_notification_message(transaction_id, old_status, new_status)
            self.notification_service.send_notification(notification_message)

    def _create_notification_message(self, transaction_id, old_status, new_status):
        # Helper method to create a notification message
        return f"Transaction {transaction_id} status changed from {old_status} to {new_status}"

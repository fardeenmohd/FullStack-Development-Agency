from typing import List

class Lead:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

class Notification:
    def __init__(self, lead_id: int, message: str):
        self.lead_id = lead_id
        self.message = message

class NotificationService:
    def send_notification(self, notification: Notification) -> None:
        print(f"Notification sent for lead {notification.lead_id}: {notification.message}")

class NotificationRepository:
    def save_notification(self, notification: Notification) -> None:
        print(f"Notification saved for lead {notification.lead_id}: {notification.message}")

class LeadService:
    def __init__(self, notification_service: NotificationService, notification_repository: NotificationRepository):
        self.notification_service = notification_service
        self.notification_repository = notification_repository

    def discover_leads(self) -> List[Lead]:
        # Simulate discovering leads
        return [Lead(1, "John Doe"), Lead(2, "Jane Smith")]

    def process_leads(self) -> None:
        for lead in self.discover_leads():
            notification = Notification(lead.id, f"New lead discovered: {lead.name}")
            self.notification_service.send_notification(notification)
            self.notification_repository.save_notification(notification)

# Example usage
if __name__ == "__main__":
    notification_service = NotificationService()
    notification_repository = NotificationRepository()
    lead_service = LeadService(notification_service, notification_repository)
    lead_service.process_leads()

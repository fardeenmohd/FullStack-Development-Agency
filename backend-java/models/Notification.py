from django.db import models

class Notification(models.Model):
    """
    Represents a notification in the system.
    
    Fields:
    - LEAD_ID: IntegerField representing the ID of the lead associated with the notification.
    - EXPORTER_ID: IntegerField representing the ID of the exporter associated with the notification.
    - NOTIFICATION_TYPE: CharField representing the type of notification, limited to 100 characters.
    - TIMESTAMP: DateTimeField automatically set to the current date and time when a new record is created.
    """
    LEAD_ID = models.IntegerField()
    EXPORTER_ID = models.IntegerField()
    NOTIFICATION_TYPE = models.CharField(max_length=100)
    TIMESTAMP = models.DateTimeField(auto_now_add=True)

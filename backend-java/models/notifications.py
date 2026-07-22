from django.db import models

class NotificationPreference(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    email_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=False)

class EventLog(models.Model):
    event_type = models.CharField(max_length=100)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class DeliveryStatus(models.Model):
    notification_preference = models.ForeignKey(NotificationPreference, on_delete=models.CASCADE)
    event_log = models.ForeignKey(EventLog, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    delivery_time = models.DateTimeField(null=True, blank=True)

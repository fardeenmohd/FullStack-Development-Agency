from django.db import models

class NotificationPreference(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    preference_key = models.CharField(max_length=100, db_index=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'preference_key')

class EventLog(models.Model):
    event_type = models.CharField(max_length=100, db_index=True)
    details = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['event_type']),
            models.Index(fields=['timestamp']),
        ]

class DeliveryStatus(models.Model):
    notification_id = models.IntegerField(db_index=True)
    delivery_method = models.CharField(max_length=50, db_index=True)
    status = models.CharField(max_length=50, choices=[('delivered', 'Delivered'), ('failed', 'Failed')], default='delivered')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['notification_id']),
            models.Index(fields=['delivery_method']),
            models.Index(fields=['status']),
            models.Index(fields=['timestamp']),
        ]

from django.db import models

class UserNotificationPreferences(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, primary_key=True)
    email_notifications_enabled = models.BooleanField(default=True)
    sms_notifications_enabled = models.BooleanField(default=False)
    push_notifications_enabled = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_notification_preferences'
        indexes = [
            models.Index(fields=['email_notifications_enabled']),
            models.Index(fields=['sms_notifications_enabled']),
            models.Index(fields=['push_notifications_enabled']),
        ]

class EventLog(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    event_type = models.CharField(max_length=100)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'event_log'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['timestamp']),
        ]

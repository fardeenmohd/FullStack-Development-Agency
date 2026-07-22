from django.db import models

class Lead(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    source = models.CharField(max_length=100, blank=True)
    score = models.IntegerField(default=0)
    last_contacted = models.DateTimeField(null=True, blank=True)
    next_follow_up = models.DateTimeField(null=True, blank=True)
    notification_sent = models.BooleanField(default=False)
    transaction_initiated = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['score']),
            models.Index(fields=['last_contacted']),
            models.Index(fields=['next_follow_up']),
            models.Index(fields=['notification_sent']),
            models.Index(fields=['transaction_initiated']),
        ]

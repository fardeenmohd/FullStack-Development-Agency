from django.db import models

class User(models.Model):
    # Define the User model if not already defined elsewhere in your project
    pass

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.event_type}"

class ExporterNotification(models.Model):
    id = models.AutoField(primary_key=True)
    lead_id = models.IntegerField()
    exporter_id = models.IntegerField()
    notification_type = models.CharField(max_length=50, choices=[('CONTACTED', 'Contacted'), ('CONVERTED', 'Converted')])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Exporter Notification for Lead {self.lead_id} - Type: {self.notification_type}"

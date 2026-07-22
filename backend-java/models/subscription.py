from django.db import models

class Subscription(models.Model):
    # Define the possible types of user milestones that can trigger a subscription event
    USER_MILESTONES = [
        ('LEVEL_UP', 'Level Up'),
        ('ACHIEVEMENT_UNLOCKED', 'Achievement Unlocked'),
        ('NEW_FEATURE', 'New Feature'),
    ]
    
    # User ID associated with the subscription
    user_id = models.IntegerField()
    
    # Type of milestone that triggered the subscription
    milestone_type = models.CharField(max_length=20, choices=USER_MILESTONES)
    
    # Flag indicating whether email notifications are enabled for this subscription
    email_notifications = models.BooleanField(default=True)
    
    # Flag indicating whether push notifications are enabled for this subscription
    push_notifications = models.BooleanField(default=False)

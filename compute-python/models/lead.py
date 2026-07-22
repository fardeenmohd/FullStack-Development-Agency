from django.db import models

class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    associated_alerts = models.ManyToManyField('alert.Alert', related_name='leads')

    def __str__(self):
        return self.name

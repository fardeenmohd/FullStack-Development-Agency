from django.db import models

class ConversionRate(models.Model):
    date = models.DateField()
    exporter_id = models.IntegerField()
    conversion_rate = models.FloatField()

    def __str__(self):
        return f"{self.date} - Exporter {self.exporter_id}: {self.conversion_rate:.2f}%"

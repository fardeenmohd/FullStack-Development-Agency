from django.db import models

class BaseSegmentedLead(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    segment_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        db_table = 'segmented_leads'

class TicketDB1SegmentedLead(BaseSegmentedLead):
    pass

class TicketDB2SegmentedLead(BaseSegmentedLead):
    pass

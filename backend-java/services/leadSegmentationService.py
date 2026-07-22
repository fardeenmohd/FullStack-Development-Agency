from models import SegmentedLead

def save_segmented_lead(data):
    try:
        segmented_lead = SegmentedLead(**data)
        segmented_lead.save()
        return True
    except Exception as e:
        print(f"Error saving segmented lead: {e}")
        return False

def save_segmented_lead_to_db(segmented_data):
    try:
        segmented_lead = SegmentedLead(**segmented_data)
        segmented_lead.save()
        return True
    except Exception as e:
        print(f"Error saving segmented lead to DB: {e}")
        return False

from typing import Optional
from models.lead import Lead
from services.notificationService import send_notification

def update_lead_status(lead_id: int, new_status: str) -> None:
    """
    Updates the status of a lead and sends a notification if the status has changed.
    
    Args:
        lead_id (int): The ID of the lead to update.
        new_status (str): The new status for the lead.
        
    Raises:
        ValueError: If the lead is not found.
    """
    # Fetch the lead from the database
    lead = get_lead_by_id(lead_id)
    
    if not lead:
        raise ValueError("Lead not found")
    
    old_status = lead.status
    
    # Update the status in the database
    update_lead_in_database(lead, new_status)
    
    # Check if the status has changed and send a notification if it has
    if old_status != new_status:
        send_notification(lead_id, f"Status updated from {old_status} to {new_status}")

def get_lead_by_id(lead_id: int) -> Optional[Lead]:
    """
    Placeholder function to fetch lead by ID.
    
    Args:
        lead_id (int): The ID of the lead to retrieve.
        
    Returns:
        Optional[Lead]: The lead object if found, otherwise None.
    """
    pass

def update_lead_in_database(lead: Lead, new_status: str) -> None:
    """
    Updates the status of a lead in the database.
    
    Args:
        lead (Lead): The lead object to update.
        new_status (str): The new status for the lead.
    """
    lead.status = new_status
    save_lead_to_database(lead)

def save_lead_to_database(lead: Lead) -> None:
    """
    Placeholder function to save lead to the database.
    
    Args:
        lead (Lead): The lead object to save.
    """
    pass

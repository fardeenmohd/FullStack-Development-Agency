from pydantic import BaseModel

class LeadAlert(BaseModel):
    """
    Represents a lead alert configuration with user-specific settings and thresholds.
    
    Attributes:
        user_id (int): The unique identifier for the user receiving the alert.
        target_regions (list[str]): A list of regions where the alert is applicable.
        product_categories (list[str]): A list of product categories to monitor.
        confidence_score_thresholds (dict[str, float]): A dictionary mapping product categories to their respective confidence score thresholds.
        alert_status (str): The current status of the alert (e.g., 'active', 'inactive').
    """
    user_id: int
    target_regions: list[str]
    product_categories: list[str]
    confidence_score_thresholds: dict[str, float]
    alert_status: str

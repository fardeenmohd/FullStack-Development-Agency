from pydantic import BaseModel

class LeadScoreModel(BaseModel):
    """
    Represents the score model for a lead, containing three key metrics:
    - Confidence Score: A measure of how certain the system is about the lead's potential.
    - Conversion Rate: The likelihood that the lead will convert into a customer.
    - Compliance Risk: The risk associated with the lead in terms of compliance regulations.
    """
    confidence_score: float
    conversion_rate: float
    compliance_risk: float

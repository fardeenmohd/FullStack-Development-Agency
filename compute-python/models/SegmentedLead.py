from pydantic import BaseModel

class SegmentedLead(BaseModel):
    """
    Represents a segmented lead with essential attributes.

    Attributes:
        lead_id (str): Unique identifier for the lead.
        country (str): Country of origin for the lead.
        industry (str): Industry sector in which the lead is interested.
        product_interest (str): Specific product or service the lead is interested in.
    """
    lead_id: str
    country: str
    industry: str
    product_interest: str

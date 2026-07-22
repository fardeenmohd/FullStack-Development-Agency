class LeadSegmentationService:
    def __init__(self, lead_data):
        self.lead_data = lead_data

    def segment_leads_by_attribute(self, attribute, value):
        """
        Segments leads based on a given attribute and value.
        
        Args:
            attribute (str): The attribute to filter by (e.g., 'country', 'industry').
            value (any): The value of the attribute to match.

        Returns:
            list: A list of lead IDs that match the criteria.
        """
        return [lead['id'] for lead in self.lead_data if lead.get(attribute) == value]

    def segment_leads_by_product_interest(self, product_interest):
        """
        Segments leads based on a specific product interest.
        
        Args:
            product_interest (str): The product interest to filter by.

        Returns:
            list: A list of lead IDs that match the criteria.
        """
        return self.segment_leads_by_attribute('product_interests', product_interest)

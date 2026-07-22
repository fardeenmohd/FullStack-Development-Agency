from typing import List, Dict

class ConversionRateService:
    def __init__(self):
        self.conversion_rates = {}

    def add_conversion_rate(self, campaign_id: str, conversion_rate: float) -> None:
        """Adds a conversion rate for a specific campaign."""
        self.conversion_rates[campaign_id] = conversion_rate

    def get_conversion_rate(self, campaign_id: str) -> float:
        """Retrieves the conversion rate for a specific campaign. Returns 0.0 if not found."""
        return self.conversion_rates.get(campaign_id, 0.0)

    def analyze_conversion_rates(self) -> Dict[str, float]:
        """Analyzes all conversion rates and returns total conversions and average conversion rate."""
        total_conversions = sum(self.conversion_rates.values())
        num_campaigns = len(self.conversion_rates)
        average_conversion_rate = total_conversions / num_campaigns if num_campaigns else 0
        return {
            'total_conversions': total_conversions,
            'average_conversion_rate': average_conversion_rate
        }

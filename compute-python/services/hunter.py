import asyncio
import uuid
import random
from typing import List
from schemas.compute import HuntLeadsRequest, LeadResponseItem

class LeadHunterService:
    # Country mapping for target regions
    REGION_MAP = {
        "OM": [("Oman", "Muscat", "om")],
        "CN": [("China", "Shanghai", "cn"), ("China", "Shenzhen", "cn")],
        "EU": [("Netherlands", "Rotterdam", "nl"), ("Germany", "Hamburg", "de"), ("France", "Marseille", "fr")],
        "AU": [("Australia", "Sydney", "au"), ("Australia", "Melbourne", "au")]
    }

    COMPANY_SUFFIXES = ["Global Trade", "Importers Ltd", "Logistics SAOC", "Holdings", "Sourcing Group", "Distribution Corp"]

    @classmethod
    async def hunt_leads(cls, request: HuntLeadsRequest) -> List[LeadResponseItem]:
        # Simulate network/scraping latency
        await asyncio.sleep(1.2)

        leads = []
        hs_prefix = request.hs_code[:2]

        # Determine industry context based on HS Code prefix
        if hs_prefix in ["10", "11", "12", "09", "07", "08"]:
            industry_keywords = ["Agro", "Foods", "Grain", "Organic", "Harvest"]
        elif hs_prefix in ["61", "62", "63", "50", "52"]:
            industry_keywords = ["Textiles", "Garments", "Apparel", "Fashion", "Threads"]
        elif hs_prefix in ["84", "85", "90"]:
            industry_keywords = ["Tech", "Machinery", "Electro", "Industrial", "Systems"]
        elif hs_prefix in ["72", "73", "74", "76"]:
            industry_keywords = ["Metals", "Steel", "Alloys", "Iron", "Forge"]
        else:
            industry_keywords = ["Global", "Merchants", "Enterprise", "Trading", "Sourcing"]

        # Generate leads based on target regions
        for region in request.target_regions:
            countries = cls.REGION_MAP.get(region.upper(), [("Oman", "Muscat", "om")])
            for country_name, city, tld in countries:
                # Randomize whether a lead is found for this specific country
                if random.random() < 0.20 and len(leads) >= 1:
                    continue

                # Generate realistic company name
                ind_word = random.choice(industry_keywords)
                suffix = random.choice(cls.COMPANY_SUFFIXES)
                company_name = f"{city} {ind_word} {suffix}"

                # Generate email
                clean_company = company_name.lower().replace(" ", "")
                contact_email = f"import@{clean_company}.{tld}"

                # Generate source URL
                source_url = f"https://{clean_company}.{tld}/partners"

                # Calculate confidence score based on HS Code match and region
                base_score = 85.0
                variance = random.uniform(-10.0, 14.0)
                confidence_score = round(min(100.0, max(50.0, base_score + variance)), 2)

                leads.append(LeadResponseItem(
                    id=uuid.uuid4(),
                    exporter_id=request.exporter_id,
                    company_name=company_name,
                    country=country_name,
                    contact_email=contact_email,
                    confidence_score=confidence_score,
                    source_url=source_url,
                    status="NEW"
                ))

        # Ensure we return at least one lead if none were generated
        if not leads:
            leads.append(LeadResponseItem(
                id=uuid.uuid4(),
                exporter_id=request.exporter_id,
                company_name="Universal Trade Alliance",
                country="Oman",
                contact_email="sourcing@universaltrade.om",
                confidence_score=88.50,
                source_url="https://universaltrade.om/partners",
                status="NEW"
            ))

        return leads

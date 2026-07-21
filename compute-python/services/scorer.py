import asyncio
from schemas.compute import ScoreLeadRequest, ScoreLeadResponse, RiskAssessment

class LeadScoringService:
    @classmethod
    async def score_lead(cls, request: ScoreLeadRequest) -> ScoreLeadResponse:
        # Simulate NLP processing latency
        await asyncio.sleep(0.8)

        company_name_lower = request.company_name.lower()
        hs_code = request.hs_code
        hs_prefix = hs_code[:2]

        # Heuristic NLP alignment score calculation
        nlp_alignment = 0.50  # Base score

        # Simple token matching
        food_keywords = ["food", "grain", "organic", "harvest", "agro", "rice", "spice", "grocer"]
        apparel_keywords = ["textile", "garment", "apparel", "fashion", "wear", "thread"]
        tech_keywords = ["tech", "machinery", "electro", "industrial", "system", "device"]
        metal_keywords = ["metal", "steel", "alloy", "iron", "forge", "copper"]

        matched = False

        if hs_prefix in ["10", "11", "12", "09", "07", "08"]:
            if any(kw in company_name_lower for kw in food_keywords):
                nlp_alignment += 0.41
                matched = True
        elif hs_prefix in ["61", "62", "63", "50", "52"]:
            if any(kw in company_name_lower for kw in apparel_keywords):
                nlp_alignment += 0.43
                matched = True
        elif hs_prefix in ["84", "85", "90"]:
            if any(kw in company_name_lower for kw in tech_keywords):
                nlp_alignment += 0.45
                matched = True
        elif hs_prefix in ["72", "73", "74", "76"]:
            if any(kw in company_name_lower for kw in metal_keywords):
                nlp_alignment += 0.38
                matched = True

        # Add some variance based on source URL presence
        if request.source_url:
            nlp_alignment += 0.05
            if any(kw in request.source_url.lower() for kw in ["partner", "b2b", "import", "trade"]):
                nlp_alignment += 0.03

        # Clamp NLP alignment score between 0.0 and 1.0
        nlp_alignment_score = round(min(1.0, max(0.1, nlp_alignment)), 2)

        # Determine risk assessment parameters
        if nlp_alignment_score >= 0.80:
            legitimacy_rating = "HIGH"
            compliance_risk = "LOW"
            sanction_check = "PASSED"
        elif nlp_alignment_score >= 0.50:
            legitimacy_rating = "MEDIUM"
            compliance_risk = "LOW"
            sanction_check = "PASSED"
        else:
            legitimacy_rating = "LOW"
            compliance_risk = "MEDIUM"
            sanction_check = "PASSED"

        # Simulate a sanction check based on company name
        if "sanctioned" in company_name_lower or "restricted" in company_name_lower:
            sanction_check = "FAILED"
            compliance_risk = "HIGH"
            legitimacy_rating = "LOW"
            nlp_alignment_score = 0.10

        # Calculate overall confidence score (0.00 to 100.00)
        if sanction_check == "FAILED":
            confidence_score = 5.0
        else:
            confidence_score = round(min(100.0, max(0.0, nlp_alignment_score * 100.0)), 2)

        # Generate analysis summary
        industry_desc = "agricultural/food products" if hs_prefix in ["10", "11", "12", "09", "07", "08"] else \
                        "textiles and apparel" if hs_prefix in ["61", "62", "63", "50", "52"] else \
                        "machinery and electronics" if hs_prefix in ["84", "85", "90"] else \
                        "industrial metals" if hs_prefix in ["72", "73", "74", "76"] else \
                        "general trade goods"

        if sanction_check == "FAILED":
            analysis_summary = "CRITICAL: Company matched potential restricted entity lists. Sanction check FAILED. Compliance risk is HIGH."
        else:
            analysis_summary = (
                f"Company has active import registries for {industry_desc} in {request.country}. "
                f"No trade sanctions found. "
                f"High alignment with HS Code {hs_code}."
            )

        return ScoreLeadResponse(
            lead_id=request.lead_id,
            confidence_score=confidence_score,
            risk_assessment=RiskAssessment(
                legitimacy_rating=legitimacy_rating,
                compliance_risk=compliance_risk,
                sanction_check=sanction_check,
                nlp_alignment_score=nlp_alignment_score
            ),
            analysis_summary=analysis_summary
        )

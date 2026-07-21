from fastapi import APIRouter, HTTPException, status
from schemas.compute import HuntLeadsRequest, HuntLeadsResponse, ScoreLeadRequest, ScoreLeadResponse
from services.hunter import LeadHunterService
from services.scorer import LeadScoringService

router = APIRouter(prefix="/compute", tags=["Compute Engine"])

@router.post(
    "/hunt-leads",
    response_model=HuntLeadsResponse,
    status_code=status.HTTP_200_OK,
    summary="Hunt Leads based on product context",
    description="Triggers the AI Lead Hunter engine to search, scrape, and identify potential buyers in target countries based on HS codes and product descriptions."
)
async def hunt_leads(payload: HuntLeadsRequest):
    try:
        leads = await LeadHunterService.hunt_leads(payload)
        return HuntLeadsResponse(
            status="success",
            leads_found=len(leads),
            data=leads
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lead hunting failed: {str(e)}"
        )

@router.post(
    "/score-lead",
    response_model=ScoreLeadResponse,
    status_code=status.HTTP_200_OK,
    summary="Score a specific lead",
    description="Evaluates and scores a specific lead's legitimacy, compliance risk, and import alignment using NLP and historical trade data."
)
async def score_lead(payload: ScoreLeadRequest):
    try:
        score_result = await LeadScoringService.score_lead(payload)
        return score_result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lead scoring failed: {str(e)}"
        )

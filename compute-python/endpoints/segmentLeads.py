from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from services.segmentation_service import SegmentLeadsService

router = APIRouter()

@router.get("/segment_leads", response_model=List[int])
async def segment_leads(criteria: str, db: Session = Depends()):
    """
    Endpoint to segment leads based on given criteria.

    Args:
        criteria (str): The criteria for segmenting leads.
        db (Session): Database session dependency.

    Returns:
        List[int]: A list of segmented lead IDs.

    Raises:
        HTTPException: If an error occurs during segmentation.
    """
    try:
        service = SegmentLeadsService()
        segmented_lead_ids = await service.segment_leads(db, criteria)
        return segmented_lead_ids
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

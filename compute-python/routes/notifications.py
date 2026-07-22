from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/subscribe/")
async def subscribe_to_notifications(exporter_id: str):
    """
    Subscribe an exporter to notification list.
    
    Args:
        exporter_id (str): The ID of the exporter to subscribe.

    Returns:
        dict: A message indicating successful subscription.

    Raises:
        HTTPException: If the exporter ID is not provided.
    """
    if not exporter_id:
        raise HTTPException(status_code=400, detail="Exporter ID is required")
    
    # Simulate adding exporter to the subscription list
    print(f"Exporter {exporter_id} subscribed to notifications.")
    
    return {"message": f"Exporter {exporter_id} has been successfully subscribed to lead status change notifications."}

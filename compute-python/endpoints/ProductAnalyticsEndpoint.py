from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.product_analytics import ProductAnalyticsResponse
from services.product_analytics_service import get_product_analytics

router = APIRouter()

@router.get("/product-analytics", response_model=ProductAnalyticsResponse)
def read_product_analytics(db: Session = Depends(get_db)):
    """
    Retrieves product analytics data.

    Args:
        db (Session): Database session dependency.

    Returns:
        ProductAnalyticsResponse: The product analytics data.

    Raises:
        HTTPException 404: If the product analytics are not found.
    """
    product_analytics = get_product_analytics(db)
    if not product_analytics:
        raise HTTPException(status_code=404, detail="Product analytics not found")
    return product_analytics

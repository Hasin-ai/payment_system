from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.exchange_rate import ExchangeRateResponse
from app.services.exchange_rate_service import ExchangeRateService

router = APIRouter()

@router.get("/{currency_code}", response_model=ExchangeRateResponse)
async def get_exchange_rate(
    currency_code: str,
    db: Session = Depends(get_db)
):
    service = ExchangeRateService(db)
    try:
        rate = await service.get_exchange_rate(currency_code.upper())
        return rate
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

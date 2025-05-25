from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import httpx
from app.models.exchange_rate import ExchangeRate
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

class ExchangeRateService:
    def __init__(self, db: Session):
        self.db = db
        self.api_url = settings.EXCHANGE_RATE_API_URL
        self.api_key = settings.EXCHANGE_RATE_API_KEY
    
    async def get_exchange_rate(self, currency_code: str) -> ExchangeRate:
        # Check cache first
        cached_rate = self.db.query(ExchangeRate).filter(
            ExchangeRate.currency_code == currency_code,
            ExchangeRate.expires_at > datetime.utcnow(),
            ExchangeRate.is_active == True
        ).first()
        
        if cached_rate:
            return cached_rate
        
        # Fetch from API
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_url}/BDT",
                    params={"access_key": self.api_key} if self.api_key else None,
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                
                if currency_code not in data.get("rates", {}):
                    raise ValueError(f"Currency {currency_code} not found")
                
                # Calculate rate to BDT
                # API returns rates from BDT to other currencies
                # We need the inverse (other currency to BDT)
                rate_from_bdt = data["rates"][currency_code]
                rate_to_bdt = 1 / rate_from_bdt
                
                # Update or create rate
                existing_rate = self.db.query(ExchangeRate).filter(
                    ExchangeRate.currency_code == currency_code
                ).first()
                
                if existing_rate:
                    existing_rate.rate_to_bdt = rate_to_bdt
                    existing_rate.last_updated = datetime.utcnow()
                    existing_rate.expires_at = datetime.utcnow() + timedelta(minutes=10)
                    existing_rate.is_active = True
                else:
                    existing_rate = ExchangeRate(
                        currency_code=currency_code,
                        rate_to_bdt=rate_to_bdt,
                        last_updated=datetime.utcnow(),
                        expires_at=datetime.utcnow() + timedelta(minutes=10),
                        is_active=True
                    )
                    self.db.add(existing_rate)
                
                self.db.commit()
                self.db.refresh(existing_rate)
                
                return existing_rate
                
        except Exception as e:
            logger.error(f"Failed to fetch exchange rate: {str(e)}")
            
            # Try to return expired rate if available
            expired_rate = self.db.query(ExchangeRate).filter(
                ExchangeRate.currency_code == currency_code
            ).first()
            
            if expired_rate:
                return expired_rate
            
            raise Exception(f"Unable to get exchange rate for {currency_code}")

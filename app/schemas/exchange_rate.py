from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime

class ExchangeRateResponse(BaseModel):
    currency_code: str
    rate_to_bdt: Decimal
    last_updated: datetime
    expires_at: datetime
    
    class Config:
        from_attributes = True

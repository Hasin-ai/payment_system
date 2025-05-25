from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, Dict, Any
from datetime import datetime
from decimal import Decimal
from app.models.transaction import TransactionStatus

class TransactionBase(BaseModel):
    requested_foreign_currency: str = Field(..., min_length=3, max_length=3)
    requested_foreign_amount: Decimal = Field(..., gt=0, decimal_places=4)
    recipient_paypal_email: EmailStr

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    status: Optional[TransactionStatus] = None
    sslcz_tran_id: Optional[str] = None
    sslcz_val_id: Optional[str] = None
    sslcz_received_bdt_amount: Optional[Decimal] = None
    sslcz_store_amount_bdt: Optional[Decimal] = None
    sslcz_card_type: Optional[str] = None
    sslcz_bank_tran_id: Optional[str] = None
    sslcz_ipn_payload: Optional[Dict[str, Any]] = None
    sslcz_validation_payload: Optional[Dict[str, Any]] = None
    paypal_payout_tran_id: Optional[str] = None
    paypal_payout_status: Optional[str] = None
    paypal_payout_payload: Optional[Dict[str, Any]] = None

class TransactionResponse(TransactionBase):
    id: int
    user_id: int
    internal_tran_id: str
    status: TransactionStatus
    exchange_rate_bdt: Decimal
    calculated_bdt_amount: Decimal
    sslcz_received_bdt_amount: Optional[Decimal]
    sslcz_store_amount_bdt: Optional[Decimal]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TransactionFilter(BaseModel):
    status: Optional[TransactionStatus] = None
    currency: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    min_amount: Optional[Decimal] = None
    max_amount: Optional[Decimal] = None

class PaymentCalculation(BaseModel):
    currency_code: str = Field(..., min_length=3, max_length=3)
    amount: Decimal = Field(..., gt=0)

class PaymentCalculationResponse(BaseModel):
    total_bdt_amount: Decimal
    exchange_rate: Decimal
    service_fee: Decimal
    currency_code: str

class PaymentInitiate(BaseModel):
    foreign_currency_code: str = Field(..., min_length=3, max_length=3)
    foreign_amount: Decimal = Field(..., gt=0)
    recipient_paypal_email: EmailStr
    
    @validator('foreign_currency_code')
    def validate_currency_code(cls, v):
        return v.upper()

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from decimal import Decimal

class PaymentIPNRequest(BaseModel):
    status: str
    tran_date: str
    tran_id: str
    val_id: str
    amount: Decimal
    store_amount: Decimal
    card_type: Optional[str] = None
    card_no: Optional[str] = None
    currency: str
    bank_tran_id: Optional[str] = None
    card_issuer: Optional[str] = None
    card_brand: Optional[str] = None
    card_issuer_country: Optional[str] = None
    card_issuer_country_code: Optional[str] = None
    currency_type: str
    currency_amount: Decimal
    value_a: Optional[str] = None
    value_b: Optional[str] = None
    value_c: Optional[str] = None
    value_d: Optional[str] = None
    verify_sign: Optional[str] = None
    verify_key: Optional[str] = None
    risk_level: Optional[int] = None
    risk_title: Optional[str] = None

class PaymentValidationResponse(BaseModel):
    status: str
    tran_date: str
    tran_id: str
    val_id: str
    amount: Decimal
    store_amount: Decimal
    currency: str
    bank_tran_id: Optional[str] = None
    card_type: Optional[str] = None
    card_no: Optional[str] = None
    card_issuer: Optional[str] = None
    card_brand: Optional[str] = None
    validated_on: Optional[str] = None

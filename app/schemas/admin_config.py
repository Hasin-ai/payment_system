from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class AdminConfigBase(BaseModel):
    admin_paypal_email: EmailStr
    admin_paypal_client_id: str = Field(..., min_length=10)
    admin_paypal_client_secret: str = Field(..., min_length=10)
    sslcz_store_id: str = Field(..., min_length=5)
    sslcz_store_passwd: str = Field(..., min_length=5)
    exchangerate_api_key: Optional[str] = None

class AdminConfigCreate(AdminConfigBase):
    pass

class AdminConfigUpdate(BaseModel):
    admin_paypal_email: Optional[EmailStr] = None
    admin_paypal_client_id: Optional[str] = None
    admin_paypal_client_secret: Optional[str] = None
    sslcz_store_id: Optional[str] = None
    sslcz_store_passwd: Optional[str] = None
    exchangerate_api_key: Optional[str] = None
    is_active: Optional[bool] = None

class AdminConfigResponse(AdminConfigBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

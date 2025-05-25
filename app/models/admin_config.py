from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class AdminConfig(Base):
    __tablename__ = "admin_config"
    
    id = Column(Integer, primary_key=True, index=True)
    admin_paypal_email = Column(String(255), nullable=False)
    admin_paypal_client_id = Column(String(255), nullable=False)
    admin_paypal_client_secret = Column(String(255), nullable=False)
    sslcz_store_id = Column(String(255), nullable=False)
    sslcz_store_passwd = Column(String(255), nullable=False)
    exchangerate_api_key = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

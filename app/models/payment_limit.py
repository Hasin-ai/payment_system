from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class PaymentLimit(Base):
    __tablename__ = "payment_limits"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    currency_code = Column(String(3), nullable=False)
    daily_limit = Column(Numeric(12, 2), nullable=False)
    monthly_limit = Column(Numeric(12, 2), nullable=False)
    yearly_limit = Column(Numeric(12, 2), nullable=False)
    current_daily_used = Column(Numeric(12, 2), default=0)
    current_monthly_used = Column(Numeric(12, 2), default=0)
    current_yearly_used = Column(Numeric(12, 2), default=0)
    daily_reset_at = Column(DateTime(timezone=True), nullable=False)
    monthly_reset_at = Column(DateTime(timezone=True), nullable=False)
    yearly_reset_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="payment_limits")

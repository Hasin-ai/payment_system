from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class TransactionStatus(str, enum.Enum):
    PENDING = "PENDING"
    IPN_RECEIVED = "IPN_RECEIVED"
    COMPLETED = "COMPLETED"
    PAYOUT_PENDING = "PAYOUT_PENDING"
    PAYOUT_COMPLETED = "PAYOUT_COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    VALIDATION_FAILED = "VALIDATION_FAILED"
    PAYOUT_FAILED = "PAYOUT_FAILED"

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    internal_tran_id = Column(String(255), unique=True, nullable=False, index=True)
    sslcz_tran_id = Column(String(255), nullable=True)
    sslcz_val_id = Column(String(255), nullable=True)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING, nullable=False)
    requested_foreign_currency = Column(String(3), nullable=False)
    requested_foreign_amount = Column(Numeric(12, 4), nullable=False)
    exchange_rate_bdt = Column(Numeric(15, 8), nullable=False)
    calculated_bdt_amount = Column(Numeric(12, 2), nullable=False)
    sslcz_received_bdt_amount = Column(Numeric(12, 2), nullable=True)
    sslcz_store_amount_bdt = Column(Numeric(12, 2), nullable=True)
    recipient_paypal_email = Column(String(255), nullable=False)
    sslcz_card_type = Column(String(100), nullable=True)
    sslcz_bank_tran_id = Column(String(100), nullable=True)
    sslcz_ipn_payload = Column(JSON, nullable=True)
    sslcz_validation_payload = Column(JSON, nullable=True)
    paypal_payout_tran_id = Column(String(255), nullable=True)
    paypal_payout_status = Column(String(50), nullable=True)
    paypal_payout_payload = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="transactions")

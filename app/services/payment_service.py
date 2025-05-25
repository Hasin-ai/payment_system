from sqlalchemy.orm import Session
from typing import Dict, Any
from app.models.transaction import Transaction, TransactionStatus

class PaymentService:
    def __init__(self, db: Session):
        self.db = db
    
    def update_transaction_status(
        self,
        transaction_id: str,
        status: TransactionStatus,
        additional_data: Dict[str, Any] = None
    ) -> Transaction:
        transaction = self.db.query(Transaction).filter(
            Transaction.internal_tran_id == transaction_id
        ).first()
        
        if not transaction:
            raise ValueError("Transaction not found")
        
        transaction.status = status
        
        if additional_data:
            for key, value in additional_data.items():
                if hasattr(transaction, key):
                    setattr(transaction, key, value)
        
        self.db.commit()
        self.db.refresh(transaction)
        
        return transaction
    
    def verify_transaction_amount(
        self,
        transaction_id: str,
        amount: float,
        currency: str = "BDT"
    ) -> bool:
        transaction = self.db.query(Transaction).filter(
            Transaction.internal_tran_id == transaction_id
        ).first()
        
        if not transaction:
            return False
        
        if currency == "BDT":
            return float(transaction.calculated_bdt_amount) == amount
        else:
            return float(transaction.requested_foreign_amount) == amount

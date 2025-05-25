from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionResponse, TransactionFilter
from app.services.transaction_service import TransactionService

class TransactionController:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.transaction_service = TransactionService(db)
    
    def get_user_transactions(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[TransactionFilter] = None
    ) -> List[TransactionResponse]:
        return self.transaction_service.get_user_transactions(
            user_id, skip, limit, filters
        )
    
    def get_transaction(self, transaction_id: str, user_id: int) -> TransactionResponse:
        transaction = self.transaction_service.get_transaction_by_id(transaction_id)
        
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        
        # Check if user owns the transaction
        if transaction.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        return transaction
    
    def get_user_stats(self, user_id: int) -> dict:
        return self.transaction_service.get_user_statistics(user_id)

from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from sqlalchemy import func, and_
from app.models.transaction import Transaction, TransactionStatus
from app.schemas.transaction import TransactionFilter

class TransactionService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_transaction_by_id(self, transaction_id: str) -> Optional[Transaction]:
        return self.db.query(Transaction).filter(
            Transaction.internal_tran_id == transaction_id
        ).first()
    
    def get_user_transactions(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[TransactionFilter] = None
    ) -> List[Transaction]:
        query = self.db.query(Transaction).filter(Transaction.user_id == user_id)
        
        if filters:
            if filters.status:
                query = query.filter(Transaction.status == filters.status)
            if filters.currency:
                query = query.filter(
                    Transaction.requested_foreign_currency == filters.currency
                )
            if filters.start_date:
                query = query.filter(Transaction.created_at >= filters.start_date)
            if filters.end_date:
                query = query.filter(Transaction.created_at <= filters.end_date)
            if filters.min_amount:
                query = query.filter(
                    Transaction.requested_foreign_amount >= filters.min_amount
                )
            if filters.max_amount:
                query = query.filter(
                    Transaction.requested_foreign_amount <= filters.max_amount
                )
        
        return query.order_by(Transaction.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_user_statistics(self, user_id: int) -> Dict:
        # Total transactions
        total_transactions = self.db.query(func.count(Transaction.id)).filter(
            Transaction.user_id == user_id
        ).scalar()
        
        # Successful transactions
        successful_transactions = self.db.query(func.count(Transaction.id)).filter(
            and_(
                Transaction.user_id == user_id,
                Transaction.status.in_([
                    TransactionStatus.COMPLETED,
                    TransactionStatus.PAYOUT_PENDING,
                    TransactionStatus.PAYOUT_COMPLETED
                ])
            )
        ).scalar()
        
        # Total amount by currency
        currency_totals = self.db.query(
            Transaction.requested_foreign_currency,
            func.sum(Transaction.requested_foreign_amount)
        ).filter(
            and_(
                Transaction.user_id == user_id,
                Transaction.status == TransactionStatus.PAYOUT_COMPLETED
            )
        ).group_by(Transaction.requested_foreign_currency).all()
        
        # Last 30 days transactions
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_transactions = self.db.query(func.count(Transaction.id)).filter(
            and_(
                Transaction.user_id == user_id,
                Transaction.created_at >= thirty_days_ago
            )
        ).scalar()
        
        return {
            "total_transactions": total_transactions,
            "successful_transactions": successful_transactions,
            "success_rate": (successful_transactions / total_transactions * 100) if total_transactions > 0 else 0,
            "currency_totals": {currency: float(amount) for currency, amount in currency_totals},
            "recent_transactions_30d": recent_transactions
        }
    
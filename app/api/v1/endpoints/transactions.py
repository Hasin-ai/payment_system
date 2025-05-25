from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.controllers.transaction_controller import TransactionController
from app.schemas.transaction import TransactionResponse, TransactionFilter
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[TransactionResponse])
def get_user_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None,
    currency: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    filters = TransactionFilter(status=status, currency=currency) if status or currency else None
    controller = TransactionController(db)
    return controller.get_user_transactions(current_user.id, skip, limit, filters)

@router.get("/stats")
def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    controller = TransactionController(db)
    return controller.get_user_stats(current_user.id)

@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    controller = TransactionController(db)
    transaction = controller.get_transaction(transaction_id, current_user.id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, payments, transactions, admin, exchange_rates

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(exchange_rates.router, prefix="/exchange-rate", tags=["Exchange Rates"])
api_router.include_router(payments.router, prefix="/payment", tags=["Payments"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])

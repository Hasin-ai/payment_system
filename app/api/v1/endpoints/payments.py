from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.controllers.payment_controller import PaymentController
from app.schemas.transaction import PaymentCalculation, PaymentCalculationResponse, PaymentInitiate
from app.schemas.payment import PaymentIPNRequest
from app.models.user import User

router = APIRouter()

@router.post("/calculate-cost", response_model=PaymentCalculationResponse)
async def calculate_cost(
    payment_calc: PaymentCalculation,
    db: Session = Depends(get_db)
):
    controller = PaymentController(db)
    return await controller.calculate_cost(payment_calc)

@router.post("/initiate")
async def initiate_payment(
    payment_data: PaymentInitiate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    controller = PaymentController(db)
    return await controller.initiate_payment(payment_data, current_user.id)

@router.post("/ipn")
async def handle_ipn(
    ipn_data: PaymentIPNRequest,
    db: Session = Depends(get_db)
):
    controller = PaymentController(db)
    return await controller.handle_ipn(ipn_data)

@router.post("/success")
async def handle_success(
    request: Request,
    db: Session = Depends(get_db)
):
    controller = PaymentController(db)
    return await controller.handle_success(request)

@router.post("/fail")
async def handle_fail(
    request: Request,
    db: Session = Depends(get_db)
):
    controller = PaymentController(db)
    return await controller.handle_fail(request)

@router.post("/cancel")
async def handle_cancel(
    request: Request,
    db: Session = Depends(get_db)
):
    controller = PaymentController(db)
    return await controller.handle_cancel(request)

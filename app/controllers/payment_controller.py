from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Dict, Any
import uuid
from app.core.database import get_db
from app.models.transaction import Transaction, TransactionStatus
from app.schemas.payment import PaymentIPNRequest, PaymentValidationResponse
from app.schemas.transaction import PaymentInitiate, PaymentCalculation, PaymentCalculationResponse
from app.services.payment_service import PaymentService
from app.services.exchange_rate_service import ExchangeRateService
from app.services.sslcommerz_service import SSLCommerzService
from app.services.paypal_service import PayPalService

class PaymentController:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.payment_service = PaymentService(db)
        self.exchange_rate_service = ExchangeRateService(db)
        self.sslcommerz_service = SSLCommerzService()
        self.paypal_service = PayPalService()
    
    async def calculate_cost(self, payment_calc: PaymentCalculation) -> PaymentCalculationResponse:
        exchange_rate = await self.exchange_rate_service.get_exchange_rate(payment_calc.currency_code)
        
        total_bdt = float(payment_calc.amount) * float(exchange_rate.rate_to_bdt)
        service_fee = total_bdt * 0.025  # 2.5% service fee
        
        return PaymentCalculationResponse(
            total_bdt_amount=total_bdt + service_fee,
            exchange_rate=exchange_rate.rate_to_bdt,
            service_fee=service_fee,
            currency_code=payment_calc.currency_code
        )
    
    async def initiate_payment(self, payment_data: PaymentInitiate, user_id: int) -> Dict[str, str]:
        # Get current exchange rate
        exchange_rate = await self.exchange_rate_service.get_exchange_rate(
            payment_data.foreign_currency_code
        )
        
        # Calculate BDT amount
        bdt_amount = float(payment_data.foreign_amount) * float(exchange_rate.rate_to_bdt)
        service_fee = bdt_amount * 0.025
        total_bdt = bdt_amount + service_fee
        
        # Create transaction
        internal_tran_id = str(uuid.uuid4())
        transaction = Transaction(
            user_id=user_id,
            internal_tran_id=internal_tran_id,
            status=TransactionStatus.PENDING,
            requested_foreign_currency=payment_data.foreign_currency_code,
            requested_foreign_amount=payment_data.foreign_amount,
            exchange_rate_bdt=exchange_rate.rate_to_bdt,
            calculated_bdt_amount=total_bdt,
            recipient_paypal_email=payment_data.recipient_paypal_email
        )
        
        self.db.add(transaction)
        self.db.commit()
        
        # Prepare SSLCommerz data
        sslcz_data = {
            "total_amount": str(total_bdt),
            "currency": "BDT",
            "tran_id": internal_tran_id,
            "success_url": "http://localhost:8000/api/v1/payment/success",
            "fail_url": "http://localhost:8000/api/v1/payment/fail",
            "cancel_url": "http://localhost:8000/api/v1/payment/cancel",
            "ipn_url": "http://localhost:8000/api/v1/payment/ipn",
            "value_a": str(payment_data.foreign_amount),
            "value_b": payment_data.foreign_currency_code,
            "value_c": payment_data.recipient_paypal_email,
            "product_name": "International Payment Transfer",
            "product_category": "Payment",
            "product_profile": "general"
        }
        
        # Initiate SSLCommerz payment
        gateway_url = await self.sslcommerz_service.create_session(sslcz_data)
        
        return {
            "redirect_url": gateway_url,
            "transaction_id": internal_tran_id
        }
    
    async def handle_ipn(self, ipn_data: PaymentIPNRequest) -> Dict[str, str]:
        # Verify transaction exists
        transaction = self.db.query(Transaction).filter(
            Transaction.internal_tran_id == ipn_data.tran_id
        ).first()
        
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        
        # Verify amount matches
        if float(transaction.calculated_bdt_amount) != float(ipn_data.amount):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Amount mismatch"
            )
        
        # Update transaction with IPN data
        transaction.status = TransactionStatus.IPN_RECEIVED
        transaction.sslcz_val_id = ipn_data.val_id
        transaction.sslcz_received_bdt_amount = ipn_data.amount
        transaction.sslcz_store_amount_bdt = ipn_data.store_amount
        transaction.sslcz_card_type = ipn_data.card_type
        transaction.sslcz_bank_tran_id = ipn_data.bank_tran_id
        transaction.sslcz_ipn_payload = ipn_data.dict()
        
        self.db.commit()
        
        return {"status": "received"}
    
    async def handle_success(self, request: Request) -> Dict[str, Any]:
        form_data = await request.form()
        tran_id = form_data.get("tran_id")
        val_id = form_data.get("val_id")
        
        if not tran_id or not val_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing transaction data"
            )
        
        # Get transaction
        transaction = self.db.query(Transaction).filter(
            Transaction.internal_tran_id == tran_id
        ).first()
        
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        
        # Validate with SSLCommerz
        validation_response = await self.sslcommerz_service.validate_transaction(val_id)
        
        if validation_response["status"] in ["VALID", "VALIDATED"]:
            # Verify transaction details
            if (validation_response["tran_id"] == tran_id and
                float(validation_response["amount"]) == float(transaction.calculated_bdt_amount) and
                validation_response["currency"] == "BDT"):
                
                # Update transaction status
                transaction.status = TransactionStatus.COMPLETED
                transaction.sslcz_validation_payload = validation_response
                self.db.commit()
                
                # Trigger PayPal payout
                try:
                    payout_response = await self.paypal_service.create_payout(
                        recipient_email=transaction.recipient_paypal_email,
                        amount=float(transaction.requested_foreign_amount),
                        currency=transaction.requested_foreign_currency,
                        reference_id=transaction.internal_tran_id
                    )
                    
                    transaction.paypal_payout_tran_id = payout_response["batch_header"]["payout_batch_id"]
                    transaction.paypal_payout_status = "PENDING"
                    transaction.paypal_payout_payload = payout_response
                    transaction.status = TransactionStatus.PAYOUT_PENDING
                    self.db.commit()
                    
                except Exception as e:
                    transaction.status = TransactionStatus.PAYOUT_FAILED
                    self.db.commit()
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Payout failed: {str(e)}"
                    )
                
                return {
                    "status": "success",
                    "message": "Payment completed successfully",
                    "transaction_id": tran_id
                }
        
        # Validation failed
        transaction.status = TransactionStatus.VALIDATION_FAILED
        self.db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment validation failed"
        )
    
    async def handle_fail(self, request: Request) -> Dict[str, str]:
        form_data = await request.form()
        tran_id = form_data.get("tran_id")
        
        if tran_id:
            transaction = self.db.query(Transaction).filter(
                Transaction.internal_tran_id == tran_id
            ).first()
            
            if transaction:
                transaction.status = TransactionStatus.FAILED
                self.db.commit()
        
        return {"status": "failed", "message": "Payment failed"}
    
    async def handle_cancel(self, request: Request) -> Dict[str, str]:
        form_data = await request.form()
        tran_id = form_data.get("tran_id")
        
        if tran_id:
            transaction = self.db.query(Transaction).filter(
                Transaction.internal_tran_id == tran_id
            ).first()
            
            if transaction:
                transaction.status = TransactionStatus.CANCELLED
                self.db.commit()
        
        return {"status": "cancelled", "message": "Payment cancelled"}

import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import logging
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.exchange_rate import ExchangeRate
from app.services.exchange_rate_service import ExchangeRateService
from app.services.payment_service import PaymentService
from app.services.paypal_service import PayPalService

logger = logging.getLogger(__name__)

class BackgroundTasks:
    def __init__(self):
        self.is_running = False
        self.tasks: Dict[str, asyncio.Task] = {}
    
    async def start(self):
        if self.is_running:
            return
        
        self.is_running = True
        self.tasks["update_exchange_rates"] = asyncio.create_task(self.update_exchange_rates_task())
        self.tasks["process_pending_payouts"] = asyncio.create_task(self.process_pending_payouts_task())
        logger.info("Background tasks started")
    
    async def stop(self):
        self.is_running = False
        for task in self.tasks.values():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        logger.info("Background tasks stopped")
    
    async def update_exchange_rates_task(self):
        db = SessionLocal()
        try:
            exchange_service = ExchangeRateService(db)
            while self.is_running:
                try:
                    # Update exchange rates every hour
                    await exchange_service.update_exchange_rates()
                    logger.info("Exchange rates updated")
                except Exception as e:
                    logger.error(f"Error updating exchange rates: {str(e)}")
                
                # Wait for 1 hour before next update
                await asyncio.sleep(3600)
        except asyncio.CancelledError:
            pass
        finally:
            db.close()
    
    async def process_pending_payouts_task(self):
        db = SessionLocal()
        try:
            payment_service = PaymentService(db)
            paypal_service = PayPalService(db)
            
            while self.is_running:
                try:
                    # Process pending payouts every 5 minutes
                    pending_payouts = db.query(Transaction).filter(
                        Transaction.status == TransactionStatus.PAYOUT_PENDING
                    ).all()
                    
                    for payout in pending_payouts:
                        try:
                            # Get payout details from PayPal
                            payout_details = await paypal_service.get_payout_details(
                                payout.paypal_payout_tran_id
                            )
                            
                            # Update transaction status based on payout status
                            if payout_details["batch_header"]["batch_status"] == "SUCCESS":
                                payout.status = TransactionStatus.PAYOUT_COMPLETED
                                payout.paypal_payout_status = "COMPLETED"
                            elif payout_details["batch_header"]["batch_status"] == "DENIED":
                                payout.status = TransactionStatus.PAYOUT_FAILED
                                payout.paypal_payout_status = "FAILED"
                            
                            payout.paypal_payout_details = payout_details
                            db.commit()
                            
                        except Exception as e:
                            logger.error(f"Error processing payout {payout.id}: {str(e)}")
                            continue
                    
                    logger.info("Processed pending payouts")
                except Exception as e:
                    logger.error(f"Error in process_pending_payouts_task: {str(e)}")
                
                # Wait for 5 minutes before next check
                await asyncio.sleep(300)
        except asyncio.CancelledError:
            pass
        finally:
            db.close()

# Global instance
background_tasks = BackgroundTasks()

# Startup and shutdown event handlers
async def startup_event():
    await background_tasks.start()

async def shutdown_event():
    await background_tasks.stop()

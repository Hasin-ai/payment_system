import httpx
import base64
from typing import Dict, Any, Optional
from app.core.config import get_settings
from app.models.admin_config import AdminConfig
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

class PayPalService:
    def __init__(self, db: Session = None):
        self.db = db
        self.base_url = settings.PAYPAL_BASE_URL
        self._access_token = None
        self._token_expires_at = None
    
    def _get_credentials(self) -> tuple:
        if self.db:
            # Get from database
            config = self.db.query(AdminConfig).filter(
                AdminConfig.is_active == True
            ).first()
            if config:
                return config.admin_paypal_client_id, config.admin_paypal_client_secret
        
        # Fallback to environment variables
        return settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET
    
    async def _get_access_token(self) -> str:
        client_id, client_secret = self._get_credentials()
        
        auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/v1/oauth2/token",
                    headers={
                        "Authorization": f"Basic {auth}",
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    data={"grant_type": "client_credentials"},
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                return data["access_token"]
                
        except Exception as e:
            logger.error(f"PayPal authentication failed: {str(e)}")
            raise
    
    async def create_payout(
        self,
        recipient_email: str,
        amount: float,
        currency: str,
        reference_id: str,
        note: Optional[str] = None
    ) -> Dict[str, Any]:
        access_token = await self._get_access_token()
        
        payout_data = {
            "sender_batch_header": {
                "sender_batch_id": reference_id,
                "email_subject": "Payment from International Transfer",
                "email_message": "You have received a payment"
            },
            "items": [{
                "recipient_type": "EMAIL",
                "amount": {
                    "value": str(amount),
                    "currency": currency
                },
                "note": note or "International payment transfer",
                "sender_item_id": reference_id,
                "receiver": recipient_email
            }]
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/v1/payments/payouts",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"
                    },
                    json=payout_data,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"PayPal payout failed: {str(e)}")
            raise
    
    async def get_payout_details(self, payout_batch_id: str) -> Dict[str, Any]:
        access_token = await self._get_access_token()
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/v1/payments/payouts/{payout_batch_id}",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"Failed to get PayPal payout details: {str(e)}")
            raise

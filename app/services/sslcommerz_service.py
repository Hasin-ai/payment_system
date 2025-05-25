import httpx
from typing import Dict, Any
from app.core.config import get_settings
from app.models.admin_config import AdminConfig
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

class SSLCommerzService:
    def __init__(self, db: Session = None):
        self.db = db
        self.base_url = settings.SSLCZ_SANDBOX_URL if settings.SSLCZ_SANDBOX_MODE else settings.SSLCZ_LIVE_URL
        
    def _get_credentials(self) -> tuple:
        if self.db:
            # Get from database
            config = self.db.query(AdminConfig).filter(
                AdminConfig.is_active == True
            ).first()
            if config:
                return config.sslcz_store_id, config.sslcz_store_passwd
        
        # Fallback to environment variables
        return settings.SSLCZ_STORE_ID, settings.SSLCZ_STORE_PASSWD
    
    async def create_session(self, payment_data: Dict[str, Any]) -> str:
        store_id, store_passwd = self._get_credentials()
        
        # Add store credentials
        payment_data.update({
            "store_id": store_id,
            "store_passwd": store_passwd,
            "cus_name": "Customer",
            "cus_email": "customer@example.com",
            "cus_phone": "01700000000",
            "cus_add1": "Dhaka",
            "cus_city": "Dhaka",
            "cus_country": "Bangladesh",
            "shipping_method": "NO",
            "num_of_item": 1,
            "emi_option": "0",
            "multi_card_name": ""
        })
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/gwprocess/v4/api.php",
                    data=payment_data,
                    timeout=30.0
                )
                response.raise_for_status()
                result = response.json()
                
                if result.get("status") == "SUCCESS":
                    return result["GatewayPageURL"]
                else:
                    raise Exception(f"SSLCommerz error: {result.get('failedreason', 'Unknown error')}")
                    
        except Exception as e:
            logger.error(f"SSLCommerz session creation failed: {str(e)}")
            raise
    
    async def validate_transaction(self, val_id: str) -> Dict[str, Any]:
        store_id, store_passwd = self._get_credentials()
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/validator/api/validationserverAPI.php",
                    params={
                        "val_id": val_id,
                        "store_id": store_id,
                        "store_passwd": store_passwd,
                        "format": "json"
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"SSLCommerz validation failed: {str(e)}")
            raise

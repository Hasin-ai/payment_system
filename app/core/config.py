from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Payment Gateway System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # SSLCommerz
    SSLCZ_STORE_ID: str
    SSLCZ_STORE_PASSWD: str
    SSLCZ_SANDBOX_URL: str = "https://sandbox.sslcommerz.com"
    SSLCZ_LIVE_URL: str = "https://securepay.sslcommerz.com"
    SSLCZ_SANDBOX_MODE: bool = True
    
    # PayPal
    PAYPAL_CLIENT_ID: str
    PAYPAL_CLIENT_SECRET: str
    PAYPAL_BASE_URL: str = "https://api.sandbox.paypal.com"
    PAYPAL_SANDBOX_MODE: bool = True
    
    # Exchange Rate API
    EXCHANGE_RATE_API_KEY: str
    EXCHANGE_RATE_API_URL: str = "https://api.exchangerate-api.com/v4/latest"
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

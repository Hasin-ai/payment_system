#!/usr/bin/env python3
import sys
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = str(Path(__file__).parent.absolute())
sys.path.insert(0, project_root)

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.user import User, UserRole
from app.models.admin_config import AdminConfig
from app.models.exchange_rate import ExchangeRate
from app.core.security import get_password_hash

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Create system admin user if not exists
        admin_user = db.query(User).filter(
            User.username == "admin"
        ).first()
        
        if not admin_user:
            admin_user = User(
                username="admin",
                email="admin@example.com",
                password_hash=get_password_hash("admin123"),
                full_name="System Administrator",
                role=UserRole.SYSTEM_ADMIN,
                is_active=True,
                is_verified=True
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            logger.info("Created system admin user")
        
        # Create default admin config if not exists
        admin_config = db.query(AdminConfig).filter(
            AdminConfig.is_active == True
        ).first()
        
        if not admin_config:
            admin_config = AdminConfig(
                admin_email="admin@example.com",
                admin_phone="+8801000000000",
                is_active=True
            )
            db.add(admin_config)
            db.commit()
            db.refresh(admin_config)
            logger.info("Created default admin config")
        
        # Add default exchange rates if not exists
        default_rates = [
            {"currency_code": "USD", "rate_to_bdt": 85.5, "last_updated": "2023-01-01"},
            {"currency_code": "EUR", "rate_to_bdt": 95.2, "last_updated": "2023-01-01"},
            {"currency_code": "GBP", "rate_to_bdt": 110.8, "last_updated": "2023-01-01"},
            {"currency_code": "CAD", "rate_to_bdt": 65.3, "last_updated": "2023-01-01"},
            {"currency_code": "AUD", "rate_to_bdt": 60.1, "last_updated": "2023-01-01"},
        ]
        
        for rate_data in default_rates:
            rate = db.query(ExchangeRate).filter(
                ExchangeRate.currency_code == rate_data["currency_code"]
            ).first()
            
            if not rate:
                rate = ExchangeRate(
                    currency_code=rate_data["currency_code"],
                    rate_to_bdt=rate_data["rate_to_bdt"],
                    last_updated=rate_data["last_updated"],
                    is_active=True
                )
                db.add(rate)
                logger.info(f"Added exchange rate for {rate_data['currency_code']}")
        
        db.commit()
        logger.info("Database initialized successfully")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error initializing database: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Done!")

from sqlalchemy.orm import Session
from typing import Optional
from app.models.admin_config import AdminConfig
from app.schemas.admin_config import AdminConfigCreate, AdminConfigUpdate

class AdminService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_active_config(self) -> Optional[AdminConfig]:
        return self.db.query(AdminConfig).filter(
            AdminConfig.is_active == True
        ).first()
    
    def create_config(self, config_data: AdminConfigCreate) -> AdminConfig:
        # Deactivate existing configs
        self.db.query(AdminConfig).update({"is_active": False})
        
        # Create new config
        db_config = AdminConfig(**config_data.dict())
        self.db.add(db_config)
        self.db.commit()
        self.db.refresh(db_config)
        
        return db_config
    
    def update_config(
        self,
        config_id: int,
        config_update: AdminConfigUpdate
    ) -> Optional[AdminConfig]:
        config = self.db.query(AdminConfig).filter(
            AdminConfig.id == config_id
        ).first()
        
        if not config:
            return None
        
        update_data = config_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(config, field, value)
        
        self.db.commit()
        self.db.refresh(config)
        
        return config

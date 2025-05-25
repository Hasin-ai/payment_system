from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.user import User, UserRole
from app.models.admin_config import AdminConfig
from app.schemas.admin_config import AdminConfigCreate, AdminConfigUpdate, AdminConfigResponse
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService
from app.services.admin_service import AdminService

class AdminController:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.user_service = UserService(db)
        self.admin_service = AdminService(db)
    
    def create_admin_user(
        self,
        user_data: UserCreate,
        current_user_role: UserRole
    ) -> UserResponse:
        if current_user_role != UserRole.SYSTEM_ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only system admin can create admin users"
            )
        
        user_data.role = UserRole.ADMIN
        return self.user_service.create_user(user_data)
    
    def get_admin_config(self) -> AdminConfigResponse:
        config = self.admin_service.get_active_config()
        if not config:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Admin configuration not found"
            )
        return config
    
    def create_admin_config(
        self,
        config_data: AdminConfigCreate,
        current_user_role: UserRole
    ) -> AdminConfigResponse:
        if current_user_role != UserRole.SYSTEM_ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only system admin can create admin configuration"
            )
        
        return self.admin_service.create_config(config_data)
    
    def update_admin_config(
        self,
        config_id: int,
        config_update: AdminConfigUpdate,
        current_user_role: UserRole
    ) -> AdminConfigResponse:
        if current_user_role != UserRole.SYSTEM_ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only system admin can update admin configuration"
            )
        
        updated_config = self.admin_service.update_config(config_id, config_update)
        if not updated_config:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Admin configuration not found"
            )
        return updated_config

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.user_service import UserService

class UserController:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.user_service = UserService(db)
    
    def create_user(self, user_data: UserCreate, current_user_role: UserRole) -> UserResponse:
        if user_data.role in [UserRole.ADMIN, UserRole.SYSTEM_ADMIN]:
            if current_user_role != UserRole.SYSTEM_ADMIN:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only system admin can create admin users"
                )
        
        return self.user_service.create_user(user_data)
    
    def get_user(self, user_id: int) -> UserResponse:
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    
    def get_users(
        self,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None
    ) -> List[UserResponse]:
        return self.user_service.get_users(skip, limit, is_active)
    
    def update_user(
        self,
        user_id: int,
        user_update: UserUpdate,
        current_user_role: UserRole
    ) -> UserResponse:
        if user_update.role and current_user_role != UserRole.SYSTEM_ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only system admin can change user roles"
            )
        
        updated_user = self.user_service.update_user(user_id, user_update)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return updated_user
    
    def delete_user(self, user_id: int, current_user_role: UserRole) -> dict:
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if user.role == UserRole.SYSTEM_ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot delete system admin"
            )
        
        self.user_service.delete_user(user_id)
        return {"message": "User deleted successfully"}

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token
from app.models.user import User
from app.schemas.user import UserLogin, Token, PasswordChange
from app.services.user_service import UserService

class AuthController:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.user_service = UserService(db)
    
    def login(self, user_login: UserLogin) -> Token:
        user = self.db.query(User).filter(
            User.username == user_login.username
        ).first()
        
        if not user or not verify_password(user_login.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is disabled"
            )
        
        access_token = create_access_token(
            data={"sub": user.username, "role": user.role.value}
        )
        refresh_token = create_refresh_token(
            data={"sub": user.username, "role": user.role.value}
        )
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            user_role=user.role
        )
    
    def change_password(self, user_id: int, password_change: PasswordChange) -> dict:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not verify_password(password_change.current_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Current password is incorrect"
            )
        
        user.password_hash = get_password_hash(password_change.new_password)
        self.db.commit()
        
        return {"message": "Password changed successfully"}

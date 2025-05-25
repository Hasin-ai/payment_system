from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.controllers.admin_controller import AdminController
from app.schemas.admin_config import AdminConfigCreate, AdminConfigUpdate, AdminConfigResponse
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User, UserRole

router = APIRouter()

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in [UserRole.ADMIN, UserRole.SYSTEM_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

def require_system_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.SYSTEM_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="System admin access required"
        )
    return current_user

@router.post("/users", response_model=UserResponse)
def create_admin_user(
    user_data: UserCreate,
    current_user: User = Depends(require_system_admin),
    db: Session = Depends(get_db)
):
    controller = AdminController(db)
    return controller.create_admin_user(user_data, current_user.role)

@router.get("/config", response_model=AdminConfigResponse)
def get_admin_config(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    controller = AdminController(db)
    return controller.get_admin_config()

@router.post("/config", response_model=AdminConfigResponse)
def create_admin_config(
    config_data: AdminConfigCreate,
    current_user: User = Depends(require_system_admin),
    db: Session = Depends(get_db)
):
    controller = AdminController(db)
    return controller.create_admin_config(config_data, current_user.role)

@router.patch("/config/{config_id}", response_model=AdminConfigResponse)
def update_admin_config(
    config_id: int,
    config_update: AdminConfigUpdate,
    current_user: User = Depends(require_system_admin),
    db: Session = Depends(get_db)
):
    controller = AdminController(db)
    return controller.update_admin_config(config_id, config_update, current_user.role)

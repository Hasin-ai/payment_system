from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.service_base import ServiceBase

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseController(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], db: Session):
        self.service = ServiceBase(model, db)
        self.db = db
    
    def get(self, id: Any) -> Optional[ModelType]:
        return self.service.get(self.db, id=id)
    
    def get_multi(
        self, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return self.service.get_multi(self.db, skip=skip, limit=limit)
    
    def create(self, obj_in: CreateSchemaType) -> ModelType:
        return self.service.create(self.db, obj_in=obj_in)
    
    def update(
        self, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        return self.service.update(self.db, db_obj=db_obj, obj_in=obj_in)
    
    def remove(self, id: int) -> ModelType:
        return self.service.remove(self.db, id=id)

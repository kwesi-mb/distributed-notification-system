# from typing import Generic, TypeVar 

# from sqlalchemy.orm import Session

# from app.db.base import Base

# ModelType = TypeVar("ModelType", bound=Base)

# class BaseRepository(Generic[ModelType]):

#     def __init__(self, db:Session, model: type[ModelType]):
#         self.db = db
#         self.model = model

#     def get_by_id(self, id: str):
#         return self.db.get(self.model, id)

#     def get_all(self):
#         return self.db.query(self.model).all()

#     def create(self, obj):
#         self.db.add(obj)
#         self.db.commit()
#         self.db.refresh(obj)
#         return obj 

#     def delete(self, obj):
#         self.db.delete(obj)
#         self.db.commit()

from typing import Generic, TypeVar 
from uuid import UUID 
from sqlalchemy.orm import Session 

from app.db.base import Base 

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):

    def __init__(
        self,
        db: Session,
        model: type[ModelType],
    ):
        self.db = db
        self.model = model

    def get_by_id(self, obj_id: UUID) -> ModelType | None:
    
            return self.db.get(
                self.model,
                obj_id,
            )
    
    def create(self, obj: ModelType) -> ModelType:

        self.db.add(obj)

        #self.db.commit()

        #self.db.refresh(obj)

        return obj 

    

    def delete(self, obj):

        self.db.delete(obj)

        self.db.commit()

    def commit(self):
        self.db.commit()

    def refresh(
            self,
            obj: ModelType,
    ):
        self.db.refresh(obj) 

    def rollback(self):
        self.db.rollback()

    def get_all(self):

        return self.db.query(
            self.model
        ).all()

    def update(self, obj):
        self.db.flush()
        self.db.refresh(obj)
        return obj

    
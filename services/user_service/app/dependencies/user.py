from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.services.cache_service import CacheService 

def get_user_service(
    db: Session = Depends(get_db),
):

    repository = UserRepository(db)

    cache = CacheService()

    return UserService(
        repository,
        cache,
    ) 
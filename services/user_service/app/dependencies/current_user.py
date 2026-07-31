from uuid import UUID

from fastapi import Depends 

from app.core.jwt import decode_token
from app.core.oauth import oauth2_scheme 
from app.dependencies.database import get_db
from app.exceptions.user import (
    InvalidCredentialsException,
    UserNotFoundException,
)
from app.repositories.user_repository import UserRepository

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db=Depends(get_db),
):

    payload = decode_token(token)

    if payload.get("type") != "access":
        raise InvalidCredentialsException()

    user_id = payload.get("sub")

    if not user_id:
        raise InvalidCredentialsException()

    repository = UserRepository(db)

    user = repository.get_by_id(
        UUID(user.id)
    )

    if not user:
        raise UserNotFoundException()

    return user
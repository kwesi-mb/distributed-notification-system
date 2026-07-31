from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from app.exceptions.user import InvalidCredentialsException 
from app.core.config import settings 


def create_access_token(
        subject: str,
        expires_delta: timedelta | None = None,
) -> str:
    expire = datetime.now(timezone.utc) + (
        expires_delta
        or timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES 
        )
    )

    payload: dict[str, Any] = {
        "sub": subject,
        "type": "access",
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM, 
    )

def create_refresh_token(
        subject: str,
) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    payload: dict[str, Any] = {
        "sub": subject,
        "type": "refresh",
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

def decode_token(token: str):

    try:

        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[
                settings.JWT_ALGORITHM
            ],
        )

        return payload 

    except JWTError:

        raise InvalidCredentialsException(
            "Invalid or expired token."
        )

        
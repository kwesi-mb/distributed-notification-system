from app.core.jwt import (
    create_access_token,
    create_refresh_token,
)
from app.core.security import verify_password
from app.exceptions.user import InvalidCredentialsException
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, TokenData
from app.core.jwt import decode_token 
class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def login(
        self,
        request: LoginRequest,
    ) -> TokenData:

        user = self.repository.get_by_email(request.email)

        if not user:
            raise InvalidCredentialsException()

        if not verify_password(
            request.password,
            user.password_hash,
        ):
            raise InvalidCredentialsException()

        return TokenData(
            access_token=create_access_token(
                str(user.id)
            ),
            refresh_token=create_refresh_token(
                str(user.id)
            ),
        )

        user.refresh_token_hash = hash_token(refresh_token)

        self.repository.commit()

        return TokenData(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def refresh(
        self,
        refresh_token: str,
    ) -> TokenData:

        payload = decode_token(refresh_token)

        if payload["type"] != "refresh":
            raise InvalidCredentialsException()

        user = self.repository.get_by_id(payload["sub"])

        if not user:
            raise UserNotFoundException()

        if not verify_token_hash(
            refresh_token,
            user.refresh_token_hash,
        ):
            raise InvalidCredentialsException()

        access_token = create_access_token(str(user.id))

        new_refresh_token = create_refresh_token(str(user.id))

        user.refresh_token_hash = hash_toke(new_refresh_token)

        self.repository.commit()

        return TokenData(
            access_token=access_token,
            refresh_token=new_refresh_token,
        )

    def logout(
        self,
        current_user: User,
    ):

        current_user.refresh_token_hash = None

        self.repository.commit()
    
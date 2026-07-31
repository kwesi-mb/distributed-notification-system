from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import CreateUserRequest
from uuid import UUID 
from app.utils.security import hash_password
from app.exceptions.user import UserNotFoundException, UserAlreadyExistsException 
from app.schemas.user import UpdateUserRequest
from math import ceil 
from app.schemas.preference import PreferenceResponse
from app.schemas.preference import (
    UpdatePreferenceRequest,
)
from app.services.cache_service import CacheService 
from app.schemas.preference import PreferenceResponse
from app.core.cache_keys import CacheKeys

class UserService:

    def __init__(
        self,
        repository: UserRepository,
        cache: CacheService,
    ):
        self.repository  = repository
        self.cache = cache

    def create_user(
        self,
        request: CreateUserRequest,
    ):

        existing = self.repository.get_by_email(
            request.email
        )

        if existing:

            raise ValueError(
                "Email already exists."
            )

        user = User(
            name=request.name,
            email=request.email,
            password_hash=hash_password(
                request.password
            ),
            push_token=request.push_token,
            email_enabled=request.preferences.email,
            push_enabled=request.preferences.push,
        )

        return self.repository.create(user)

    def get_user(self, user_id: UUID):

        user = self.repository.get_by_id(user_id)

        if not user:
            raise UserNotFoundException()

        return user

    def list_users(
            self,
            page: int,
            limit: int,
            search: str | None,
            sort_by: str,
            order: str,
    ):

        users, total = self.repository.get_users(
            page,
            limit,
            search,
            sort_by,
            order,
        )

        meta = {
            "total": total,
            "limit": limit,
            "page": page,
            "total_pages": ceil(total / limit),
            "has_next": page * limit < total,
            "has_previous": page > 1,
        }

        return users, meta

    def update_user(
        self,
        user_id: UUID,
        request: UpdateUserRequest,
    ):
        user = self.repository.get_by_id(user_id)

        if not user:
            raise UserNotFoundException()

        if request.email:

            existing = self.repository.get_by_email(
                request.email 
            )

            if existing and existing.id != user.id:
                raise UserAlreadyExistsException()

            user.email = request.email

        if request.name:
            user.name = request.name

        if request.password:
            user.password_hash = hash_password(
                request.password
            )

        if request.push_token is not None:
            user.push_token = request.push_token

        if request.email_enabled is not None:
            user.email_enabled = request.email_enabled

        if request.push_enabled is not None:
            user.push_enabled = request.push_enabled 

        self.repository.update(user)

        self.repository.commit()

        return user 

    def delete_user(
        self,
        user_id: UUID,
    ):

        user = self.repository.get_by_id(user_id)

        if not user:
            raise UserNotFoundException()

        self.repository.delete(user)

        self.repository.commit()

    def get_preferences(
        self,
        current_user,
    ) -> PreferenceResponse:

        cache_key = CacheKeys.preferences(
            str(current_user.id)
        )

        cached = self.cache.get(cache_key)

        if cached:

            return PreferenceResponse(
                **cached 
            )

        preferences = PreferenceResponse(
            email=current_user.email_enabled,
            push=current_user.push_enabled,
        )

        self.cache.set(
            cache_key,
            preferences.model_dump(),
        )

        return preferences 

    def update_preferences(
        self,
        current_user,
        request: UpdatePreferenceRequest,
    ):

        if request.email is not None:
            current_user.email_enabled = request.email

        if request.push is not None:
            current_user.push_enabled = request.push 

        self.repository.commit()

        self.repository.refresh(current_user)

        self.cache.delete(
            CacheKeys.preferences(
                str(current_user.id)
            )
        )

        return current_user
        
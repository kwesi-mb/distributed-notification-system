from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import CreateUserRequest
from app.utils.security import hash_password 

class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, request: CreateUserRequest):

        existing = self.repository.get_by_email(request.email)

        if existing:
            raise ValueError("Email already exists.")

        user = User(
            name=request.name,
            email=request.email,
            password_hash=hash_password(request.password),
            push_token=request.push_token,
            email_enabled=request.preferences.email,
            push_enabled=request.preferences.push,
        )

        return self.repository.create(user)
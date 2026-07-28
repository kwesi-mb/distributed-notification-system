from fastapi import APIRouter, Depends, HTTPException

from app.schemas.user import CreateUserRequest
from app.services.user_service import UserService
from app.dependencies.user import get_user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/")
def create_user(
    request: CreateUserRequest,
    service: UserService = Depends(get_user_service),
):

    try:

        user = service.create_user(request)

        return {
            "success": True,
            "data": user,
            "message": "User created successfully.",
            "error": None,
            "meta": None,
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
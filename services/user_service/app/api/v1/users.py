import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent

project_root = current_dir.parents[4]

shared_path = project_root / "shared"
sys.path.append(str(shared_path))

from responses.response import success_response 
#from shared.responses.response import success_response
from fastapi import APIRouter, Depends, HTTPException, Query 
from uuid import UUID

from app.dependencies.user import get_user_service
from app.schemas.user import CreateUserRequest, UpdateUserRequest 
from app.schemas.user import UserResponse
from app.services.user_service import UserService
from app.dependencies.current_user import (
    get_current_user,
)
from app.schemas.preference import (
    PreferenceResponse,
)
from app.schemas.preference import (
    UpdatePreferenceRequest,
)


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.post(
    "/",
    response_model=UserResponse,
)
def create_user(
    request: CreateUserRequest,
    service: UserService = Depends(
        get_user_service
    ),
):

    try:

        user = service.create_user(
            request 
        )

        response = UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            push_token=user.push_token,
            preferences={
                "email": user.email_enabled,
                "push": user.push_enabled,
            },
            created_at=user.created_at,
        )

        return success_response(
            data=response, 
            message="User created successfully.",
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

@router.get("/{user_id}")
def get_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
):

    user = service.get_user(user_id)

    return success_response(
        data=UserResponse.model_validate(user),
        message="User retrieved successfully."
    )

@router.get("/")
def list_users(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    search: str | None = None,
    sort_by: str = "created_at",
    order: str = "desc",
    service: UserService = Depends(get_user_service),
):

    users, meta = service.list_users(
        page,
        limit,
        search,
        sort_by,
        order,
    )

    return success_response(
        data=[
            UserResponse.model_validate(user)
            for user in users 
        ],
        message="Users retrieved successfully.",
        meta=meta,
    )

@router.patch("/{user_id}")
def update_user(
    user_id: UUID,
    request: UpdateUserRequest,
    service: UserService = Depends(
        get_user_service,
    ),
):

    user = service.update_user(
        user_id,
        request,
    )

    return success_response(
        data=UserResponse.model_validate(user),
        message="User updated successfully.",
    )

@router.delete("/{user_id}")
def delete_user(
    user_id: UUID,
    service: UserService = Depends(
        get_user_service,
    ),
):

    service.delete_user(user_id)

    return success_response(
        data=None,
        message="User deleted successfully."
    )

@router.get("/me/preferences")
def get_preferences(

    current_user=Depends(
        get_current_user,
    ),

    service: UserService = Depends(
        get_user_service,
    ),
):

    preferences = service.get_preferences(
        current_user
    )

    return success_response(

        data=preferences,

        message="Preferences retrieved successfully.",
    )

@router.patch("/me/preferences")
def update_preferences(

    request: UpdatePreferenceRequest,

    current_user=Depends(
        get_current_user,
    ),

    service: UserService = Depends(
        get_user_service,
    ),
):

    user = service.update_preferences(
        current_user,
        request,
    )

    return success_response(

        data=PreferenceResponse(

            email=user.email_enabled,

            push=user.push_enabled,

        ),

        message="Preferences updated successfully.",
    )
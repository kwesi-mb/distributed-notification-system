import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent

project_root = current_dir.parents[4]

shared_path = project_root / "shared"
sys.path.append(str(shared_path))

from responses.response import success_response 
from fastapi import APIRouter, Depends
from pydantic import BaseModel 
from app.dependencies.auth import get_auth_service
from app.schemas.auth import LoginRequest
from app.services.auth_service import AuthService
#from shared.responses.response import success_response 
from app.dependencies.current_user import (
    get_current_user,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("login")
def login(
    request: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    tokens = service.login(request)

    return success_response(
        data=tokens,
        message="Login successful."
    )

@router.get("/me")
def me(

    current_user=Depends(
        get_current_user
    ),

):

    return success_response(

        data=UserResponse.model_validate(
            current_user
        ),

        message="Current user retrieved successfully."
    )

class RefreshRequest(BaseModel):
    refresh_token: str

@router.post("/refresh")
def refresh_token(
    request: RefreshRequest,
    service: AuthService = Depends(get_auth_service),
):

    tokens = service.refresh(
        request.refresh_token
    )

    return success_response(
        data=tokens,
        message="Token refreshed successfully."
    )

@router.post("/logout")
def logout(
    current_user: User = Depends(get_current_user),
    service: AuthService = Depends(get_auth_service),
):

    service.logout(current_user)

    return success_response(
        data=None,
        message="Logged out successfully."
    )
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")

class PaginationMeta(BaseModel):
    total: int = 0
    limit: int = 0
    page: int = 1
    total_pages: int = 1
    has_next: bool = False
    has_previous: bool = False

class APIResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    message: str 
    meta: Optional[PaginationMeta] = None 


def success_response(
    data: Any = None,
    message: str = "Success",
    meta: Optional[PaginationMeta] = None,
) -> APIResponse:
    return APIResponse(
        success=True,
        data=data,
        error=None,
        message=message,
        meta=meta,
    )

def error_response(
    message: str,
    error: str,
) -> APIResponse:
    return APIResponse(
        success=False,
        data=None,
        error=error,
        message=message,
        meta=None,
    )

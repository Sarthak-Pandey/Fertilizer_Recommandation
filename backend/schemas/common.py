"""
Common response schemas including error responses and generic paginated responses.
"""

from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class ErrorResponse(BaseModel):
    """Standard error response payload."""
    success: bool = False
    error: str = Field(..., description="Error summary message")
    detail: Optional[str] = Field(None, description="Detailed error message or stack trace info")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic reusable paginated response model."""
    items: List[T] = Field(default_factory=list, description="List of paginated items")
    total: int = Field(0, ge=0, description="Total number of items across all pages")
    page: int = Field(1, ge=1, description="Current page number")
    per_page: int = Field(20, ge=1, le=100, description="Number of items per page")
    total_pages: int = Field(0, ge=0, description="Total number of pages")

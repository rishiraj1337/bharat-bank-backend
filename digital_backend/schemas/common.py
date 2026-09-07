from typing import Optional, Generic, TypeVar, Any, List
from datetime import datetime
from pydantic import BaseModel, Field

T = TypeVar("T")

class BaseApiResponse(BaseModel):
    success: bool = Field(default=True, example=True, description="Indicates whether the request was successful")
    response_code: str = Field(default="BB-200", example="BB-200", description="Bank standard response status code")
    message: str = Field(default="Operation completed successfully", example="Operation completed successfully")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z", example="2026-09-07T06:30:00Z")


class ApiResponse(BaseApiResponse, Generic[T]):
    data: Optional[T] = None


class PaginatedMetadata(BaseModel):
    total_records: int = Field(..., example=42, description="Total count of records matching criteria")
    page: int = Field(default=1, example=1, description="Current page number (1-indexed)")
    page_size: int = Field(default=10, example=10, description="Number of items per page")
    total_pages: int = Field(..., example=5, description="Total pages available")
    has_next: bool = Field(default=False, example=True)
    has_prev: bool = Field(default=False, example=False)


class ErrorDetail(BaseModel):
    code: str = Field(..., example="INVALID_BENEFICIARY")
    message: str = Field(..., example="The recipient account number is invalid or blocked")
    field: Optional[str] = Field(default=None, example="beneficiary_account_no")


class ApiErrorResponse(BaseModel):
    success: bool = Field(default=False, example=False)
    response_code: str = Field(default="BB-ERR-400", example="BB-ERR-400")
    message: str = Field(..., example="Validation failed")
    errors: Optional[List[ErrorDetail]] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

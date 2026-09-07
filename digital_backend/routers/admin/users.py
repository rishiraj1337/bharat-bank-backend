from fastapi import APIRouter, HTTPException, status
from typing import List
import uuid
from digital_backend.schemas.common import ApiResponse, BaseApiResponse
from digital_backend.schemas.admin_schemas import (
    AdminUserItem,
    AdminUserCreateRequest,
    AdminRoleItem
)
from digital_backend.mock_store import mock_db

router = APIRouter(prefix="/users", tags=["1. Admin User & Role Management (US-20)"])

@router.get("", response_model=ApiResponse[List[AdminUserItem]], summary="List All Admin Users")
async def list_admin_users():
    """
    Lists bank operations and administrative staff users (PRD US-20).
    """
    items = [AdminUserItem(**u) for u in mock_db.admin_users]
    return ApiResponse(data=items, message="Admin users list fetched")


@router.post("", response_model=ApiResponse[AdminUserItem], summary="Create New Admin User")
async def create_admin_user(payload: AdminUserCreateRequest):
    """
    Creates an administrative user with role-based access control.
    """
    user_id = f"ADM-{uuid.uuid4().hex[:4].upper()}"
    new_user = {
        "user_id": user_id,
        "username": payload.username,
        "full_name": payload.full_name,
        "email": payload.email,
        "role": payload.role,
        "department": payload.department,
        "branch_code": payload.branch_code,
        "is_active": True,
        "last_login_at": "Never",
        "created_at": "2026-09-07T06:30:00Z"
    }
    mock_db.admin_users.append(new_user)
    return ApiResponse(data=AdminUserItem(**new_user), message="Admin user created successfully")


@router.get("/roles", response_model=ApiResponse[List[AdminRoleItem]], summary="List Available Roles & Permission Sets")
async def list_admin_roles():
    """
    Returns security roles and their assigned granular system permissions.
    """
    roles = [AdminRoleItem(**r) for r in mock_db.admin_roles]
    return ApiResponse(data=roles, message="Roles list retrieved")


@router.put("/{user_id}/toggle-active", response_model=BaseApiResponse, summary="Toggle Admin User Active Status")
async def toggle_admin_user_active(user_id: str):
    """
    Activate or deactivate bank administrator account.
    """
    for u in mock_db.admin_users:
        if u["user_id"] == user_id:
            u["is_active"] = not u["is_active"]
            status_text = "activated" if u["is_active"] else "deactivated"
            return BaseApiResponse(success=True, response_code="BB-200", message=f"User {u['username']} {status_text}.")
    raise HTTPException(status_code=404, detail="Admin user not found")

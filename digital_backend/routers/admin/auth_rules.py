from fastapi import APIRouter, HTTPException, status
from typing import List
import uuid
from digital_backend.schemas.common import ApiResponse, BaseApiResponse
from digital_backend.schemas.admin_schemas import (
    AuthorizationRuleItem,
    CreateAuthRuleRequest,
    CorporateHierarchyNode
)
from digital_backend.mock_store import mock_db

router = APIRouter(prefix="/auth-rules", tags=["3. Admin Authorization Matrix & Corporate Hierarchies (US-22)"])

@router.get("", response_model=ApiResponse[List[AuthorizationRuleItem]], summary="List Authorization Matrix Rules")
async def list_auth_rules():
    """
    Returns configured maker-checker approval rules, threshold limits, and tiers (PRD US-22).
    """
    items = [AuthorizationRuleItem(**r) for r in mock_db.auth_rules]
    return ApiResponse(data=items, message="Authorization rules retrieved")


@router.post("", response_model=ApiResponse[AuthorizationRuleItem], summary="Create / Update Authorization Rule")
async def create_auth_rule(payload: CreateAuthRuleRequest):
    """
    Configure new maker-checker threshold policy for corporate or retail payments.
    """
    rule_id = f"RULE-{uuid.uuid4().hex[:6].upper()}"
    new_rule = {
        "rule_id": rule_id,
        "rule_name": payload.rule_name,
        "client_segment": payload.client_segment,
        "min_amount": payload.min_amount,
        "max_amount": payload.max_amount,
        "maker_role_required": payload.maker_role_required,
        "checker_role_required": payload.checker_role_required,
        "required_approvals_count": payload.required_approvals_count,
        "cooling_period_hours": payload.cooling_period_hours,
        "is_active": True,
        "version": 1,
        "updated_by": "rajesh.amin",
        "updated_at": "2026-09-07T06:30:00Z"
    }
    mock_db.auth_rules.append(new_rule)
    return ApiResponse(data=AuthorizationRuleItem(**new_rule), message="Authorization rule created")


@router.get("/corporate-hierarchies", response_model=ApiResponse[List[CorporateHierarchyNode]], summary="List Corporate Client Hierarchies (US-03)")
async def list_corporate_hierarchies():
    """
    Lists corporate organizational hierarchies, role limits, and authorization levels (PRD US-03).
    """
    items = [CorporateHierarchyNode(**n) for n in mock_db.corporate_hierarchies]
    return ApiResponse(data=items, message="Corporate hierarchies fetched")

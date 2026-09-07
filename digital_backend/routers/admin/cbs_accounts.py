from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
from digital_backend.schemas.common import ApiResponse, BaseApiResponse
from digital_backend.schemas.admin_schemas import (
    AdminAccountItem,
    AccountFreezeActionRequest,
    AccountUnfreezeActionRequest,
    AccountLienItem,
    MarkLienRequest,
    BalanceAdjustmentRequest
)
from digital_backend.mock_store import mock_db

router = APIRouter(prefix="/cbs-accounts", tags=["7. Admin CBS Account Servicing & Controls"])

@router.get("", response_model=ApiResponse[List[AdminAccountItem]], summary="Search & Inquire All CBS Accounts")
async def list_cbs_accounts(
    account_type: Optional[str] = Query(default=None, description="SAVINGS, CURRENT, SALARY"),
    status: Optional[str] = Query(default=None, description="ACTIVE, FROZEN_DEBIT, FROZEN_TOTAL"),
    branch_code: Optional[str] = Query(default=None, description="Branch code e.g. 001, 002")
):
    """
    Direct backoffice inquiry across CBS accounts repository with balances and statuses.
    """
    items = []
    for acc in mock_db.accounts.values():
        if account_type and acc["account_type_code"] != account_type:
            continue
        if branch_code and acc.get("branch_code") != branch_code:
            continue
        cust = mock_db.customers.get(acc["cif"], {})
        items.append(AdminAccountItem(
            account_number=acc["account_number"],
            cif=acc["cif"],
            customer_name=cust.get("name", "Bharat Bank Customer"),
            account_type=acc["account_type_code"],
            product_code=acc.get("product_code", "SB001"),
            available_balance=acc["available_balance"],
            ledger_balance=acc["ledger_balance"],
            lien_amount=acc.get("lien_amount", 0.0),
            status=acc["status"].upper(),
            branch_code=acc.get("branch_code", "001"),
            branch_name=acc.get("branch_name", "Nariman Point Branch"),
            ifsc=acc.get("ifsc", "APEX0001048"),
            currency=acc.get("currency", "INR"),
            open_date=acc.get("open_date", "2024-01-15")
        ))
    return ApiResponse(data=items, message="CBS accounts fetched")


@router.post("/{account_number}/freeze", response_model=BaseApiResponse, summary="CBS Account Freeze Action (DEBIT / CREDIT / TOTAL)")
async def freeze_account(account_number: str, payload: AccountFreezeActionRequest):
    """
    Mirrors CBS v3 `/cbs/account/freeze` contract:
    Locks account for Debits, Credits, or Total with CBS compliance audit reason.
    """
    acc = mock_db.accounts.get(account_number)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found in CBS")

    acc["status"] = f"FROZEN_{payload.freeze_type}"
    acc["freeze_reason"] = payload.reason_code

    # Audit log
    mock_db.audit_logs.insert(0, {
        "log_id": f"AUDIT-FRZ-{account_number}",
        "timestamp": "2026-09-07T06:30:00Z",
        "admin_user": "rajesh.amin",
        "action_type": "CBS_ACCOUNT_FREEZE",
        "target_resource_id": account_number,
        "ip_address": "10.20.4.115",
        "new_value": {"freeze_type": payload.freeze_type, "reason": payload.reason_code, "remarks": payload.remarks},
        "status": "SUCCESS"
    })

    return BaseApiResponse(
        success=True,
        response_code="BB-200",
        message=f"Account {account_number} successfully placed on {payload.freeze_type} freeze in CBS. Reason: {payload.reason_code}."
    )


@router.post("/{account_number}/unfreeze", response_model=BaseApiResponse, summary="CBS Account Unfreeze Action")
async def unfreeze_account(account_number: str, payload: AccountUnfreezeActionRequest):
    """
    Mirrors CBS v3 `/cbs/account/unfreeze` contract:
    Restores frozen account to ACTIVE status.
    """
    acc = mock_db.accounts.get(account_number)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found in CBS")

    acc["status"] = "Active"
    acc["freeze_reason"] = None

    mock_db.audit_logs.insert(0, {
        "log_id": f"AUDIT-UNFRZ-{account_number}",
        "timestamp": "2026-09-07T06:30:00Z",
        "admin_user": "priya.sharma",
        "action_type": "CBS_ACCOUNT_UNFREEZE",
        "target_resource_id": account_number,
        "ip_address": "10.20.4.116",
        "new_value": {"status": "ACTIVE", "reason": payload.reason_code},
        "status": "SUCCESS"
    })

    return BaseApiResponse(
        success=True,
        response_code="BB-200",
        message=f"Account {account_number} successfully restored to ACTIVE in CBS."
    )


@router.get("/{account_number}/liens", response_model=ApiResponse[List[AccountLienItem]], summary="Get Account Active Liens")
async def get_account_liens(account_number: str):
    """
    Inquires active collateral and court attachment lien holds.
    """
    liens = [AccountLienItem(**l) for l in getattr(mock_db, "account_liens", []) if l["account_number"] == account_number]
    return ApiResponse(data=liens, message="Active liens fetched")


@router.post("/{account_number}/liens", response_model=ApiResponse[AccountLienItem], summary="Mark New Lien / Hold on Account")
async def mark_account_lien(account_number: str, payload: MarkLienRequest):
    """
    Earmarks and restricts specified available balance as lien hold.
    """
    acc = mock_db.accounts.get(account_number)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")

    if acc["available_balance"] < payload.lien_amount:
        raise HTTPException(status_code=400, detail="Insufficient available balance to mark lien")

    acc["available_balance"] -= payload.lien_amount
    acc["lien_amount"] = acc.get("lien_amount", 0.0) + payload.lien_amount

    new_lien = {
        "lien_id": f"LIEN-00{len(mock_db.account_liens)+1}",
        "account_number": account_number,
        "lien_amount": payload.lien_amount,
        "reason": payload.reason,
        "marked_by": "rajesh.amin",
        "marked_at": "2026-09-07T06:30:00Z",
        "status": "ACTIVE"
    }
    mock_db.account_liens.append(new_lien)

    return ApiResponse(data=AccountLienItem(**new_lien), message="Lien successfully marked in CBS")


@router.delete("/{account_number}/liens/{lien_id}", response_model=BaseApiResponse, summary="Remove / Release Account Lien")
async def remove_account_lien(account_number: str, lien_id: str):
    """
    Releases lien hold and restores available balance.
    """
    acc = mock_db.accounts.get(account_number)
    released = False
    for l in mock_db.account_liens:
        if l["lien_id"] == lien_id and l["account_number"] == account_number:
            if acc:
                acc["available_balance"] += l["lien_amount"]
                acc["lien_amount"] = max(0.0, acc.get("lien_amount", 0.0) - l["lien_amount"])
            l["status"] = "RELEASED"
            released = True
            break
    if not released:
        raise HTTPException(status_code=404, detail="Lien record not found")

    return BaseApiResponse(success=True, response_code="BB-200", message=f"Lien {lien_id} released successfully.")


@router.post("/{account_number}/balance-adjustment", response_model=ApiResponse[dict], summary="Maker-Checker Manual Balance Adjustment")
async def manual_balance_adjustment(account_number: str, payload: BalanceAdjustmentRequest):
    """
    Backoffice ledger credit/debit adjustment against general ledger suspense accounts with checker approval.
    """
    acc = mock_db.accounts.get(account_number)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")

    if payload.adjustment_type == "CREDIT":
        acc["available_balance"] += payload.amount
        acc["ledger_balance"] += payload.amount
    else:
        acc["available_balance"] -= payload.amount
        acc["ledger_balance"] -= payload.amount

    return ApiResponse(
        data={
            "account_number": account_number,
            "adjustment_type": payload.adjustment_type,
            "amount": payload.amount,
            "gl_suspense_code": payload.gl_code,
            "new_available_balance": acc["available_balance"],
            "checker_status": "APPROVED",
            "audit_ref": "ADJ-20260907-9912"
        },
        message="Manual balance adjustment executed in CBS"
    )

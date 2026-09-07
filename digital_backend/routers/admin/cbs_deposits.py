from fastapi import APIRouter, HTTPException, Query, status
from typing import List
from digital_backend.schemas.common import ApiResponse, BaseApiResponse
from digital_backend.schemas.flutter_schemas import TermDepositAccountItem
from digital_backend.mock_store import mock_db

router = APIRouter(prefix="/cbs-deposits", tags=["12. Admin Term Deposits & Tax Exemption Ops (CBS v3)"])

@router.get("", response_model=ApiResponse[List[TermDepositAccountItem]], summary="List All Customer Term Deposits")
async def list_all_deposits():
    """
    Backoffice inquiry of Fixed Deposits and Recurring Deposits across all branches.
    """
    items = [TermDepositAccountItem(**d) for d in mock_db.deposits]
    return ApiResponse(data=items, message="Deposits retrieved")


@router.get("/{deposit_id}/trial-closure", response_model=ApiResponse[dict], summary="TD Trial Pre-closure (Mirrors CBS v3 td_trial_closure)")
async def trial_pre_closure(deposit_id: str):
    """
    Mirrors CBS v3 `/cbs/td/trial/closure`:
    Computes pre-closure penalty, interest accrued to date, and net payable before executing premature withdrawal.
    """
    for d in mock_db.deposits:
        if d["deposit_id"] == deposit_id:
            principal = d["principal_amount"]
            penalty = round(principal * 0.005, 2)  # 0.5% premature penalty
            accrued_interest = round(principal * 0.045, 2)
            net_payable = principal + accrued_interest - penalty
            return ApiResponse(
                data={
                    "deposit_id": deposit_id,
                    "account_number": d["account_number"],
                    "principal_amount": principal,
                    "closure_value": principal + accrued_interest,
                    "penalty_amount": penalty,
                    "net_payable": net_payable,
                    "currency": "INR",
                    "cbs_status": "CALCULATED"
                },
                message="Trial closure calculation complete"
            )
    raise HTTPException(status_code=404, detail="Deposit not found")


@router.post("/{deposit_id}/force-close", response_model=ApiResponse[dict], summary="Execute Premature Deposit Closure")
async def force_close_deposit(deposit_id: str, credit_account_number: str = "101000000012"):
    """
    Executes premature deposit closure in CBS and credits net payout to customer savings account.
    """
    for d in mock_db.deposits:
        if d["deposit_id"] == deposit_id:
            d["status"] = "CLOSED"
            payout = d["principal_amount"] + 3500.0  # net payout
            acc = mock_db.accounts.get(credit_account_number)
            if acc:
                acc["available_balance"] += payout
                acc["ledger_balance"] += payout
            return ApiResponse(
                data={
                    "deposit_id": deposit_id,
                    "payout_amount": payout,
                    "credited_to_account": credit_account_number,
                    "cbs_reference": "TD-CLOSURE-99128",
                    "closure_status": "SETTLED"
                },
                message="Term deposit closed prematurely and funds disbursed."
            )
    raise HTTPException(status_code=404, detail="Deposit not found")

from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
from digital_backend.schemas.common import ApiResponse, BaseApiResponse
from digital_backend.schemas.admin_schemas import (
    InwardChequeClearingItem,
    ChequeClearingActionRequest,
    ChequeBookInventoryItem
)
from digital_backend.mock_store import mock_db

router = APIRouter(prefix="/cbs-cheques", tags=["9. Admin Cheque Clearing & CTS House Operations (CBS v3)"])

@router.get("/inward-clearing", response_model=ApiResponse[List[InwardChequeClearingItem]], summary="Inward CTS Clearing Batch Queue")
async def get_inward_cheques(
    clearing_cycle: Optional[str] = Query(default=None, description="CTS GRID 1, CTS GRID 2")
):
    """
    Mirrors CBS v3 Cheque Clearing:
    Fetches incoming CTS clearing cheques presented by other banks awaiting debit authorization.
    """
    items = [InwardChequeClearingItem(**c) for c in getattr(mock_db, "inward_cheques", [])]
    if clearing_cycle:
        items = [c for c in items if c.clearing_cycle == clearing_cycle]
    return ApiResponse(data=items, message="Inward CTS clearing queue fetched")


@router.post("/inward-clearing/{cheque_id}/action", response_model=BaseApiResponse, summary="Action Inward Cheque (Clear or Return)")
async def action_inward_cheque(cheque_id: str, payload: ChequeClearingActionRequest):
    """
    Authorizes clearing settlement or returns cheque with RBI CTS return reason codes.
    """
    for c in mock_db.inward_cheques:
        if c["cheque_id"] == cheque_id:
            c["status"] = "CLEARED" if payload.action == "CLEAR" else "RETURNED"
            
            # If cleared, deduct funds
            if payload.action == "CLEAR":
                acc = mock_db.accounts.get(c["drawer_account_number"])
                if acc:
                    acc["available_balance"] -= c["amount"]
                    acc["ledger_balance"] -= c["amount"]

            msg = f"Cheque #{c['cheque_number']} {payload.action.lower()}ed."
            if payload.return_reason_code:
                msg += f" Return Reason: {payload.return_reason_code}."

            return BaseApiResponse(success=True, response_code="BB-200", message=msg)
            
    raise HTTPException(status_code=404, detail="Cheque item not found in clearing queue")


@router.get("/inventory", response_model=ApiResponse[List[ChequeBookInventoryItem]], summary="Branch Cheque Book Inventory Stock")
async def get_cheque_inventory():
    """
    Inquires branch vault stock of personalized and non-personalized cheque books.
    """
    items = [ChequeBookInventoryItem(**inv) for inv in getattr(mock_db, "cheque_inventory", [])]
    return ApiResponse(data=items, message="Cheque inventory stock loaded")


@router.post("/inventory/replenish", response_model=BaseApiResponse, summary="Replenish Branch Cheque Book Stock")
async def replenish_cheque_inventory(branch_code: str, leaves_25: int = 50, leaves_50: int = 50, leaves_100: int = 25):
    """
    Records stock replenishment from security printing press into branch vault.
    """
    for inv in mock_db.cheque_inventory:
        if inv["branch_code"] == branch_code:
            inv["stock_25_leaves"] += leaves_25
            inv["stock_50_leaves"] += leaves_50
            inv["stock_100_leaves"] += leaves_100
            inv["last_replenished_on"] = "2026-09-07"
            return BaseApiResponse(success=True, response_code="BB-200", message="Inventory replenished successfully.")
    raise HTTPException(status_code=404, detail="Branch not found")

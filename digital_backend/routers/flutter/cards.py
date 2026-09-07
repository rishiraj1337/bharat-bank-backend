from fastapi import APIRouter, HTTPException, status
from typing import List
from digital_backend.schemas.common import ApiResponse, BaseApiResponse
from digital_backend.schemas.flutter_schemas import (
    CardDetailItem,
    CardLockToggleRequest,
    CardBlockRequest,
    CardBillPaymentRequest
)
from digital_backend.mock_store import mock_db

router = APIRouter(prefix="/cards", tags=["7. App Cards Management"])

@router.get("", response_model=ApiResponse[List[CardDetailItem]], summary="List All Debit & Credit Cards")
async def list_cards():
    """
    Returns customer's Credit and Debit cards with real-time status and spend limits.
    """
    items = [CardDetailItem(**c) for c in mock_db.cards]
    return ApiResponse(data=items, message="Cards retrieved successfully")


@router.post("/{card_id}/lock-toggle", response_model=BaseApiResponse, summary="Instant Lock / Unlock Card")
async def toggle_card_lock(card_id: str, payload: CardLockToggleRequest):
    """
    Instantly locks or unlocks card for security (PRD US-16).
    """
    for c in mock_db.cards:
        if c["card_id"] == card_id:
            c["is_locked"] = payload.is_locked
            state = "locked" if payload.is_locked else "unlocked"
            return BaseApiResponse(success=True, response_code="BB-200", message=f"Card has been successfully {state}.")
    raise HTTPException(status_code=404, detail="Card not found")


@router.post("/{card_id}/block", response_model=BaseApiResponse, summary="Permanent Card Block & Hotlisting")
async def block_card(card_id: str, payload: CardBlockRequest):
    """
    Permanent hotlisting of lost or stolen debit/credit cards with re-issuance request.
    """
    for c in mock_db.cards:
        if c["card_id"] == card_id:
            c["is_blocked"] = True
            c["is_locked"] = True
            msg = f"Card blocked permanently due to '{payload.reason}'."
            if payload.reissue_requested:
                msg += " Replacement card will be dispatched to your registered address."
            return BaseApiResponse(success=True, response_code="BB-200", message=msg)
    raise HTTPException(status_code=404, detail="Card not found")


@router.post("/{card_id}/pay-bill", response_model=ApiResponse[dict], summary="Pay Credit Card Bill (Screen 1 Match)")
async def pay_credit_card_bill(card_id: str, payload: CardBillPaymentRequest):
    """
    Pay outstanding dues on Signature Mastercard (due ₹67,500).
    """
    debit_acc = mock_db.accounts.get(payload.debit_account_number)
    if not debit_acc:
        raise HTTPException(status_code=404, detail="Debit account not found")

    if debit_acc["available_balance"] < payload.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds in selected account")

    debit_acc["available_balance"] -= payload.amount

    for c in mock_db.cards:
        if c["card_id"] == card_id and c["card_type"] == "CREDIT":
            c["outstanding_due"] = max(0.0, c["outstanding_due"] - payload.amount)
            c["formatted_outstanding_due"] = f"₹{c['outstanding_due']:,.0f}"

    return ApiResponse(
        data={
            "card_id": card_id,
            "paid_amount": payload.amount,
            "remaining_due": 0.0,
            "payment_reference": "CCPAY-20260907-9912",
            "receipt_url": "https://receipts.bharatbank.com/cc/CCPAY-20260907-9912.pdf"
        },
        message="Credit Card bill payment successful"
    )

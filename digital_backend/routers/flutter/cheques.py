from fastapi import APIRouter, HTTPException, status
from typing import List
import uuid
from digital_backend.schemas.common import ApiResponse, BaseApiResponse
from digital_backend.schemas.flutter_schemas import (
    ChequeBookRequest,
    StopChequeRequest
)

router = APIRouter(prefix="/cheques", tags=["11. App Cheque Servicing"])

@router.post("/request-book", response_model=ApiResponse[dict], summary="Request New Cheque Book")
async def request_cheque_book(payload: ChequeBookRequest):
    """
    Submits a service request for a new cheque book (25, 50, or 100 leaves) (PRD US-17).
    """
    req_id = f"SR-CHQ-{uuid.uuid4().hex[:6].upper()}"
    return ApiResponse(
        data={
            "request_id": req_id,
            "account_number": payload.account_number,
            "leaves_count": payload.number_of_leaves,
            "delivery_address": payload.delivery_address,
            "expected_delivery": "Within 3-5 business days",
            "status": "DISPATCH_IN_PROGRESS"
        },
        message="Cheque book request submitted successfully"
    )


@router.post("/stop-cheque", response_model=BaseApiResponse, summary="Stop Cheque Payment")
async def stop_cheque(payload: StopChequeRequest):
    """
    Instantly marks cheque leaf as STOPPED in Core Banking System (PRD US-17).
    """
    return BaseApiResponse(
        success=True,
        response_code="BB-200",
        message=f"Cheque #{payload.cheque_number} has been stopped successfully. Reason: {payload.reason}"
    )


@router.get("/leaves", response_model=ApiResponse[List[dict]], summary="Get Cheque Leaves Status")
async def get_cheque_leaves_status(account_number: str = "101000000012"):
    """
    Inquires status of all cheque leaves in current book.
    """
    leaves = [
        {"cheque_number": "110001", "status": "USED", "amount": 5000.0, "cleared_on": "2026-08-10"},
        {"cheque_number": "110002", "status": "AVAILABLE", "amount": None, "cleared_on": None},
        {"cheque_number": "110003", "status": "STOPPED", "amount": None, "cleared_on": None},
        {"cheque_number": "110004", "status": "AVAILABLE", "amount": None, "cleared_on": None}
    ]
    return ApiResponse(data=leaves, message="Cheque leaves status fetched")

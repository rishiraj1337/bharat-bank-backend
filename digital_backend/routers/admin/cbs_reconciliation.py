from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
from digital_backend.schemas.common import ApiResponse, BaseApiResponse
from digital_backend.schemas.admin_schemas import (
    SettlementBatchItem,
    ReconciliationExceptionItem
)
from digital_backend.mock_store import mock_db

router = APIRouter(prefix="/cbs-reconciliation", tags=["11. Admin Daily Settlement & NPCI Reconciliation"])

@router.get("/batches", response_model=ApiResponse[List[SettlementBatchItem]], summary="List Daily Clearing Batches (IMPS/NEFT/RTGS/BBPS)")
async def list_settlement_batches(
    payment_rail: Optional[str] = Query(default=None, description="IMPS, NEFT, RTGS, BBPS")
):
    """
    Inquires central switch clearing cycles, total volume, matched vs discrepancy transactions.
    """
    items = [SettlementBatchItem(**b) for b in getattr(mock_db, "settlement_batches", [])]
    if payment_rail:
        items = [b for b in items if b.payment_rail == payment_rail]
    return ApiResponse(data=items, message="Settlement batches loaded")


@router.post("/batches/{batch_id}/reconcile", response_model=ApiResponse[dict], summary="Run Automated Batch Reconciliation")
async def run_batch_reconciliation(batch_id: str):
    """
    Triggers automated 3-way reconciliation (CBS Ledger vs NPST Switch vs NPCI Central Settlement File).
    """
    for b in mock_db.settlement_batches:
        if b["batch_id"] == batch_id:
            b["status"] = "RECONCILED"
            b["matched_txns"] = b["total_txns"]
            b["unreconciled_txns"] = 0
            return ApiResponse(
                data={
                    "batch_id": batch_id,
                    "reconciliation_status": "COMPLETED",
                    "matched_count": b["matched_txns"],
                    "unresolved_exceptions": 0,
                    "net_clearing_amount": b["total_volume"]
                },
                message=f"Batch {batch_id} reconciled successfully."
            )
    raise HTTPException(status_code=404, detail="Batch not found")


@router.get("/exceptions", response_model=ApiResponse[List[ReconciliationExceptionItem]], summary="List Reconciliation Discrepancies & Exceptions")
async def list_reconciliation_exceptions():
    """
    Lists transactions with status mismatches (e.g. CBS timeout while NPCI debited).
    """
    items = [ReconciliationExceptionItem(**e) for e in getattr(mock_db, "reconciliation_exceptions", [])]
    return ApiResponse(data=items, message="Reconciliation exceptions loaded")


@router.post("/exceptions/{exception_id}/resolve", response_model=BaseApiResponse, summary="Resolve Exception / Post Adjustment")
async def resolve_exception(exception_id: str, action: str = "AUTO_REFUND", remarks: str = "Refund posted to customer account"):
    """
    Executes automated refund or manual ledger adjustment to resolve reconciliation exception.
    """
    for e in mock_db.reconciliation_exceptions:
        if e["exception_id"] == exception_id:
            e["resolution_status"] = "RESOLVED"
            return BaseApiResponse(
                success=True,
                response_code="BB-200",
                message=f"Exception {exception_id} resolved via {action}. Remarks: {remarks}."
            )
    raise HTTPException(status_code=404, detail="Exception not found")

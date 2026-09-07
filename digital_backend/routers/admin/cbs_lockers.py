from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
from digital_backend.schemas.common import ApiResponse, BaseApiResponse
from digital_backend.schemas.admin_schemas import (
    BranchDetailItem,
    LockerInventoryItem,
    LockerAllotmentRequest
)
from digital_backend.mock_store import mock_db

router = APIRouter(prefix="/cbs-branches-lockers", tags=["10. Admin Branches & Safe Deposit Lockers (CBS v3)"])

@router.get("/branches", response_model=ApiResponse[List[BranchDetailItem]], summary="CBS Branch Master Directory")
async def list_branches():
    """
    Returns CBS branch directory, vault cash holding, and locker capacities.
    """
    items = [BranchDetailItem(**b) for b in getattr(mock_db, "branches", [])]
    return ApiResponse(data=items, message="Branches retrieved")


@router.get("/lockers", response_model=ApiResponse[List[LockerInventoryItem]], summary="Locker Inventory Inquiry (CBS v3 locker_inquiry)")
async def list_lockers(
    branch_code: str = Query(default="001", description="Branch identifier e.g. 001"),
    status: Optional[str] = Query(default=None, description="AVAILABLE, OCCUPIED")
):
    """
    Mirrors CBS v3 `/cbs/locker/inquiry`:
    Inquires Safe Deposit Lockers availability, rental matrix (SMALL, MEDIUM, LARGE, EXTRA_LARGE).
    """
    items = [LockerInventoryItem(**l) for l in getattr(mock_db, "lockers", []) if l["branch_code"] == branch_code]
    if status:
        items = [l for l in items if l.status == status]
    return ApiResponse(data=items, message="Locker inventory fetched")


@router.post("/lockers/allot", response_model=ApiResponse[dict], summary="Allot Locker to Customer CIF")
async def allot_locker(payload: LockerAllotmentRequest):
    """
    Allots vacant locker to customer CIF, registers operating instructions, and collects annual rent.
    """
    cust = mock_db.customers.get(payload.cif)
    if not cust:
        raise HTTPException(status_code=404, detail="Customer CIF not found")

    for l in mock_db.lockers:
        if l["locker_id"] == payload.locker_id:
            if l["status"] == "OCCUPIED":
                raise HTTPException(status_code=400, detail="Locker is already occupied")
            l["status"] = "OCCUPIED"
            l["allotted_to_cif"] = payload.cif
            l["allotment_date"] = "2026-09-07"
            
            return ApiResponse(
                data={
                    "locker_id": payload.locker_id,
                    "cif": payload.cif,
                    "customer_name": cust["name"],
                    "annual_rent_debited": l["annual_rent"],
                    "agreement_number": f"AGR-LCK-{payload.locker_id}",
                    "allotment_status": "CONFIRMED"
                },
                message="Locker allotted successfully"
            )
    raise HTTPException(status_code=404, detail="Locker ID not found")

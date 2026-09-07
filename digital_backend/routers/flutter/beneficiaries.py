from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
import uuid
from digital_backend.schemas.common import ApiResponse, BaseApiResponse
from digital_backend.schemas.flutter_schemas import (
    BeneficiaryItem,
    AddBeneficiaryRequest
)
from digital_backend.mock_store import mock_db

router = APIRouter(prefix="/beneficiaries", tags=["6. App Beneficiary Management"])

@router.get("", response_model=ApiResponse[List[BeneficiaryItem]], summary="List Saved Beneficiaries (Screen 3 Match)")
async def list_beneficiaries(
    search: Optional[str] = Query(default=None, description="Search by name, bank, or account number")
):
    """
    Returns list of saved payees matching Screenshot 3:
    1. Sneha Mehta (Bharat Co-operative Bank · **** **** 9182)
    2. Rohan Deshmukh (HDFC Bank · **** **** 8239)
    3. Amitabh Bachchan (ICICI Bank · **** **** 0007)
    4. ABC Suppliers Ltd. (HDFC Bank · **** 7821)
    5. Amazon Web Services (Citibank · **** 8182)
    """
    items = [BeneficiaryItem(**b) for b in mock_db.beneficiaries]
    if search:
        s = search.lower()
        items = [
            b for b in items 
            if s in b.name.lower() or s in b.bank_name.lower() or s in b.masked_account_number
        ]
    return ApiResponse(data=items, message="Beneficiaries list fetched")


@router.post("", response_model=ApiResponse[BeneficiaryItem], summary="Add New Beneficiary")
async def add_beneficiary(payload: AddBeneficiaryRequest):
    """
    Add and register a new beneficiary with OTP verification and configurable cooling-off period.
    """
    if payload.account_number != payload.confirm_account_number:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "ACCOUNT_MISMATCH", "message": "Account number and confirmation account number do not match"}
        )

    initials = "".join([part[0].upper() for part in payload.name.split()[:2]])
    masked = f"**** **** {payload.account_number[-4:]}"
    
    new_bene = {
        "beneficiary_id": f"BEN-{uuid.uuid4().hex[:4].upper()}",
        "cif": "CIF100001",
        "name": payload.name,
        "bank_name": payload.bank_name or "Partner Bank",
        "account_number": payload.account_number,
        "masked_account_number": masked,
        "ifsc": payload.ifsc.upper(),
        "account_type": payload.account_type or "SAVINGS",
        "transfer_type": "IMPS",
        "avatar_initials": initials,
        "is_within_bank": "APEX" in payload.ifsc.upper(),
        "cooling_period_active": True,
        "max_transfer_limit": 50000.00
    }
    
    mock_db.beneficiaries.append(new_bene)
    return ApiResponse(
        data=BeneficiaryItem(**new_bene),
        message="Beneficiary added successfully. 30-minute cooling period active with ₹50,000 max limit."
    )


@router.get("/{beneficiary_id}", response_model=ApiResponse[BeneficiaryItem], summary="Get Beneficiary Details")
async def get_beneficiary(beneficiary_id: str):
    """
    Fetch specific beneficiary record by ID.
    """
    for b in mock_db.beneficiaries:
        if b["beneficiary_id"] == beneficiary_id:
            return ApiResponse(data=BeneficiaryItem(**b), message="Beneficiary found")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"code": "NOT_FOUND", "message": f"Beneficiary {beneficiary_id} not found"}
    )


@router.delete("/{beneficiary_id}", response_model=BaseApiResponse, summary="Delete Beneficiary")
async def delete_beneficiary(beneficiary_id: str):
    """
    Removes beneficiary from customer's saved payee directory.
    """
    initial_len = len(mock_db.beneficiaries)
    mock_db.beneficiaries = [b for b in mock_db.beneficiaries if b["beneficiary_id"] != beneficiary_id]
    if len(mock_db.beneficiaries) == initial_len:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": f"Beneficiary {beneficiary_id} not found"}
        )
    return BaseApiResponse(success=True, response_code="BB-200", message="Beneficiary removed successfully")


@router.post("/validate-account", response_model=ApiResponse[dict], summary="Penny-Drop Account Verification")
async def validate_account(account_number: str, ifsc: str):
    """
    Performs NPCI penny-drop account validation before payee registration.
    """
    return ApiResponse(
        data={
            "account_number": account_number,
            "ifsc": ifsc,
            "registered_beneficiary_name": "SNEHA R MEHTA",
            "account_status": "ACTIVE_VALID",
            "bank_name": "Bharat Co-operative Bank",
            "is_name_match": True,
            "confidence_score": 98.5
        },
        message="Beneficiary account verified via penny drop"
    )

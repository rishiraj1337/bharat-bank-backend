from fastapi import APIRouter, HTTPException, status
from typing import List
from digital_backend.schemas.common import ApiResponse, BaseApiResponse
from digital_backend.schemas.flutter_schemas import (
    NomineeDetail,
    NachMandateItem
)
from digital_backend.mock_store import mock_db

router = APIRouter(prefix="/services", tags=["12. App Banking Utilities & Services"])

@router.get("/nominee", response_model=ApiResponse[NomineeDetail], summary="Get Account Nominee Details")
async def get_nominee(account_number: str = "101000000012"):
    """
    Inquires registered nominee for savings or term deposit account.
    """
    nominee = NomineeDetail(
        name="Sneha Mehta",
        relation="SPOUSE",
        date_of_birth="1994-08-22",
        share_percentage=100,
        address="102, Palm Heights, Bandra West, Mumbai 400050"
    )
    return ApiResponse(data=nominee, message="Nominee details fetched")


@router.put("/nominee", response_model=BaseApiResponse, summary="Update Account Nominee Details")
async def update_nominee(account_number: str, payload: NomineeDetail):
    """
    Updates registered nominee with OTP confirmation.
    """
    return BaseApiResponse(success=True, response_code="BB-200", message="Nominee updated successfully")


@router.get("/share-ifsc", response_model=ApiResponse[dict], summary="Get Shareable Account & IFSC Card")
async def share_ifsc(account_number: str = "101000000012"):
    """
    Generates shareable payload with Account Number, IFSC, UPI ID, and QR code string.
    """
    acc = mock_db.accounts.get(account_number, list(mock_db.accounts.values())[0])
    return ApiResponse(
        data={
            "account_holder_name": "Arjun Mehta",
            "account_number": acc["account_number"],
            "masked_account_number": acc["masked_account_number"],
            "ifsc": acc["ifsc"],
            "bank_name": "Bharat Bank",
            "branch_name": acc["branch_name"],
            "upi_id": "arjun.mehta@bharatbank",
            "share_text": f"Bank: Bharat Bank\nA/C: {acc['account_number']}\nIFSC: {acc['ifsc']}\nBranch: {acc['branch_name']}\nName: Arjun Mehta",
            "qr_data": f"upi://pay?pa=arjun.mehta@bharatbank&pn=Arjun%20Mehta&cu=INR"
        },
        message="Shareable details prepared"
    )


@router.get("/nach-mandates", response_model=ApiResponse[List[NachMandateItem]], summary="Get Active NACH / e-Mandates")
async def get_nach_mandates():
    """
    Lists registered eNACH recurring debits for insurance, mutual funds, and loans.
    """
    mandates = [
        NachMandateItem(
            mandate_id="UMRN-NACH-8829104",
            beneficiary_corporate="HDFC Life Insurance Co.",
            debit_account_number="101000000012",
            max_amount=25000.00,
            frequency="MONTHLY",
            start_date="2025-01-01",
            end_date="2035-01-01",
            status="ACTIVE"
        ),
        NachMandateItem(
            mandate_id="UMRN-NACH-9910283",
            beneficiary_corporate="Bharat Mutual Fund AMC",
            debit_account_number="101000000012",
            max_amount=15000.00,
            frequency="MONTHLY",
            start_date="2024-06-01",
            end_date="2029-06-01",
            status="ACTIVE"
        )
    ]
    return ApiResponse(data=mandates, message="NACH mandates retrieved")


@router.get("/epassbook", response_model=ApiResponse[dict], summary="Digital ePassbook View")
async def get_epassbook(account_number: str = "101000000012"):
    """
    Offline-first synchronized passbook entries for mobile client.
    """
    acc = mock_db.accounts.get(account_number, list(mock_db.accounts.values())[0])
    return ApiResponse(
        data={
            "account_number": acc["account_number"],
            "holder_name": "Arjun Mehta",
            "passbook_sync_timestamp": "2026-09-07T06:30:00Z",
            "entries": mock_db.transactions
        },
        message="ePassbook synchronized"
    )


@router.get("/certificates/interest", response_model=ApiResponse[dict], summary="Download Interest Certificate (Form 16A)")
async def get_interest_certificate(year: str = "2026"):
    """
    Generates downloadable annual interest certificate for tax filing (PRD US-13).
    """
    return ApiResponse(
        data={
            "cif": "CIF100001",
            "customer_name": "Arjun Mehta",
            "financial_year": year,
            "savings_interest_earned": 15432.56,
            "term_deposit_interest_earned": 14500.00,
            "total_interest_earned": 29932.56,
            "tds_deducted": 2993.26,
            "download_url": f"https://tax.bharatbank.com/certificates/interest_{year}_CIF100001.pdf"
        },
        message="Interest certificate generated"
    )


@router.get("/certificates/tds", response_model=ApiResponse[dict], summary="Download TDS Certificate (Form 26AS)")
async def get_tds_certificate(year: str = "2026"):
    """
    Generates downloadable TDS deduction tax certificate (PRD US-13).
    """
    return ApiResponse(
        data={
            "cif": "CIF100001",
            "pan_number": "ABCDE1234F",
            "financial_year": year,
            "total_tds_deposited": 2993.26,
            "download_url": f"https://tax.bharatbank.com/certificates/tds_form26as_{year}_CIF100001.pdf"
        },
        message="TDS certificate generated"
    )

from fastapi import APIRouter, HTTPException, status
from typing import List
import uuid
from digital_backend.schemas.common import ApiResponse, BaseApiResponse
from digital_backend.schemas.flutter_schemas import (
    LoanAccountItem,
    RepaymentScheduleItem,
    StandingInstructionRequest,
    LoanApplicationRequest,
    PreApprovedOffer
)
from digital_backend.mock_store import mock_db

router = APIRouter(prefix="/loans", tags=["9. App Loans & Borrowings"])

@router.get("", response_model=ApiResponse[List[LoanAccountItem]], summary="List Active Loans")
async def list_loans():
    """
    Returns customer's active loans, principal balance, interest rate, and next EMI date (PRD US-14).
    """
    items = [LoanAccountItem(**ln) for ln in mock_db.loans]
    return ApiResponse(data=items, message="Loans retrieved")


@router.get("/offers", response_model=ApiResponse[List[PreApprovedOffer]], summary="Get Pre-Approved Loan Offers (Banner Match)")
async def get_loan_offers():
    """
    Returns personalized instant pre-approved credit and loan offers (e.g. Instant Personal Loan up to ₹5,00,000).
    """
    offers = [PreApprovedOffer(**p) for p in mock_db.pre_approved_offers]
    return ApiResponse(data=offers, message="Pre-approved offers fetched")


@router.get("/{loan_id}/repayment-schedule", response_model=ApiResponse[List[RepaymentScheduleItem]], summary="Get Loan Repayment Amortization Schedule")
async def get_repayment_schedule(loan_id: str):
    """
    Returns month-by-month principal and interest breakdown.
    """
    schedule = [
        RepaymentScheduleItem(installment_no=1, due_date="2026-09-10", principal_component=13308.00, interest_component=30083.00, total_installment=43391.00, ending_balance=4236692.00, status="UPCOMING"),
        RepaymentScheduleItem(installment_no=2, due_date="2026-10-10", principal_component=13402.00, interest_component=29989.00, total_installment=43391.00, ending_balance=4223290.00, status="UPCOMING"),
        RepaymentScheduleItem(installment_no=3, due_date="2026-11-10", principal_component=13497.00, interest_component=29894.00, total_installment=43391.00, ending_balance=4209793.00, status="UPCOMING")
    ]
    return ApiResponse(data=schedule, message="Amortization schedule loaded")


@router.post("/{loan_id}/standing-instruction", response_model=BaseApiResponse, summary="Set EMI Auto-Debit Standing Instruction")
async def set_loan_standing_instruction(loan_id: str, payload: StandingInstructionRequest):
    """
    Configures auto-pay standing instruction for recurring loan EMI debit (PRD US-15).
    """
    return BaseApiResponse(
        success=True,
        response_code="BB-200",
        message=f"Auto-debit Standing Instruction active for account {payload.debit_account_number} on day {payload.debit_day_of_month} of each month."
    )


@router.post("/apply", response_model=ApiResponse[dict], summary="Apply for New Loan")
async def apply_loan(payload: LoanApplicationRequest):
    """
    Submits new retail loan application.
    """
    app_no = f"LNAPP-{uuid.uuid4().hex[:6].upper()}"
    return ApiResponse(
        data={
            "application_number": app_no,
            "status": "IN_REVIEW",
            "requested_amount": payload.requested_amount,
            "estimated_emi": round(payload.requested_amount * 0.032, 2),
            "next_step": "A loan officer will verify your documents within 24 hours."
        },
        message="Loan application submitted successfully"
    )

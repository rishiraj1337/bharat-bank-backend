from fastapi import APIRouter, HTTPException, status
from typing import List
import uuid
from datetime import datetime, timedelta

from digital_backend.schemas.common import ApiResponse, BaseApiResponse
from digital_backend.schemas.flutter_schemas import (
    TermDepositAccountItem,
    TermDepositRateItem,
    TermDepositCalculateRequest,
    TermDepositCalculateResponse,
    OpenDepositRequest,
    OpenRecurringDepositRequest
)
from digital_backend.mock_store import mock_db

router = APIRouter(prefix="/deposits", tags=["8. App Term Deposits (FD & RD) (v2)"])


@router.get("", response_model=ApiResponse[List[TermDepositAccountItem]], summary="List Customer Term Deposits")
async def list_deposits():
    """
    Returns active Fixed Deposits and Recurring Deposits with maturity dates and yields.
    """
    items = [TermDepositAccountItem(**d) for d in mock_db.deposits]
    return ApiResponse(data=items, message="Deposits fetched")


@router.get("/rates", response_model=ApiResponse[List[TermDepositRateItem]], summary="Get Live Term Deposit Rates Table")
async def get_deposit_rates():
    """
    Fetches interest rate slabs for General Public and Senior Citizens.
    """
    rates = [
        TermDepositRateItem(tenure_min_days=7, tenure_max_days=45, tenure_label="7 days to 45 days", general_interest_rate=4.50, senior_citizen_interest_rate=5.00),
        TermDepositRateItem(tenure_min_days=46, tenure_max_days=179, tenure_label="46 days to 179 days", general_interest_rate=5.75, senior_citizen_interest_rate=6.25),
        TermDepositRateItem(tenure_min_days=180, tenure_max_days=364, tenure_label="180 days to 364 days", general_interest_rate=6.50, senior_citizen_interest_rate=7.00),
        TermDepositRateItem(tenure_min_days=365, tenure_max_days=443, tenure_label="1 Year to 443 Days", general_interest_rate=7.10, senior_citizen_interest_rate=7.60),
        TermDepositRateItem(tenure_min_days=444, tenure_max_days=444, tenure_label="444 Days Special Monsoon", general_interest_rate=7.75, senior_citizen_interest_rate=8.25),
        TermDepositRateItem(tenure_min_days=445, tenure_max_days=1825, tenure_label="2 Years to 5 Years", general_interest_rate=7.25, senior_citizen_interest_rate=7.75)
    ]
    return ApiResponse(data=rates, message="Interest rate slabs retrieved")


@router.post("/calculate", response_model=ApiResponse[TermDepositCalculateResponse], summary="Calculate FD/RD Maturity & Interest")
async def calculate_deposit(payload: TermDepositCalculateRequest):
    """
    Computes exact maturity amount and interest earned for chosen tenure and deposit amount.
    """
    rate = 7.75 if payload.tenure_months == 15 else (7.10 if payload.tenure_months <= 12 else 7.25)
    if payload.is_senior_citizen:
        rate += 0.50

    interest_earned = round(payload.amount * (rate / 100) * (payload.tenure_months / 12), 2)
    maturity_amount = payload.amount + interest_earned

    res = TermDepositCalculateResponse(
        principal_amount=payload.amount,
        tenure_months=payload.tenure_months,
        interest_rate=rate,
        interest_earned=interest_earned,
        maturity_amount=maturity_amount,
        maturity_date="2027-09-07"
    )
    return ApiResponse(data=res, message="Calculation complete")


@router.post("/open-fd", response_model=ApiResponse[TermDepositAccountItem], summary="Open Online Fixed Deposit (FD)")
async def open_fixed_deposit(payload: OpenDepositRequest):
    """
    Instantly debits funding account and creates Fixed Deposit (PRD US-12).
    """
    debit_acc = mock_db.accounts.get(payload.debit_account_number)
    if not debit_acc or debit_acc["available_balance"] < payload.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds in debit account")

    debit_acc["available_balance"] -= payload.amount

    rate = 7.10 if payload.tenure_months <= 12 else 7.25
    interest = round(payload.amount * (rate / 100) * (payload.tenure_months / 12), 2)
    maturity_amt = payload.amount + interest

    fd_id = f"FD-{uuid.uuid4().hex[:6].upper()}"
    new_fd = {
        "deposit_id": fd_id,
        "cif": "CIF100001",
        "account_number": fd_id.replace("-", ""),
        "deposit_type": "FIXED_DEPOSIT",
        "principal_amount": payload.amount,
        "formatted_principal": f"₹{payload.amount:,.2f}",
        "interest_rate": rate,
        "maturity_amount": maturity_amt,
        "formatted_maturity": f"₹{maturity_amt:,.2f}",
        "deposit_date": datetime.utcnow().strftime("%Y-%m-%d"),
        "maturity_date": "2027-09-07",
        "tenure_months": payload.tenure_months,
        "interest_payout_mode": payload.interest_payout,
        "auto_renewal": payload.auto_renewal,
        "nominee_name": payload.nominee_name or "Sneha Mehta",
        "status": "ACTIVE"
    }
    mock_db.deposits.append(new_fd)
    return ApiResponse(data=TermDepositAccountItem(**new_fd), message="Fixed Deposit created successfully")


@router.get("/{deposit_id}/advice", response_model=ApiResponse[dict], summary="Download FD Deposit Advice PDF")
async def download_deposit_advice(deposit_id: str):
    """
    Generates official bank fixed deposit advice certificate (PRD US-12).
    """
    return ApiResponse(
        data={
            "deposit_id": deposit_id,
            "document_title": f"Fixed Deposit Advice Certificate - {deposit_id}",
            "download_url": f"https://documents.bharatbank.com/fd/advice/{deposit_id}.pdf",
            "file_size_kb": 164.2
        },
        message="Deposit advice ready for download"
    )


# --- NEW IN V2: OPEN RECURRING DEPOSIT ---
@router.post("/open-rd", response_model=ApiResponse[TermDepositAccountItem], summary="Open Online Recurring Deposit (RD)")
async def open_recurring_deposit(payload: OpenRecurringDepositRequest):
    """
    Opens a Recurring Deposit (RD) account with automated monthly debit.
    - Debits first monthly installment immediately from the selected account.
    - Sets up standing instruction for subsequent installment debits.
    - Computes maturity yield using standardized compound interest.
    """
    debit_acc = mock_db.accounts.get(payload.debit_account_number)
    if not debit_acc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "ACCOUNT_NOT_FOUND", "message": f"Debit account {payload.debit_account_number} not found"}
        )

    if debit_acc["available_balance"] < payload.monthly_installment_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INSUFFICIENT_FUNDS", "message": f"Insufficient balance for first monthly installment of ₹{payload.monthly_installment_amount:,.2f}"}
        )

    # Debit first month installment
    debit_acc["available_balance"] -= payload.monthly_installment_amount

    # Determine rate and maturity for RD
    n = payload.tenure_months
    p = payload.monthly_installment_amount
    rate = 7.10 if n <= 12 else (7.25 if n <= 24 else 7.50)

    # Standard Indian Banking RD Compound Interest Formula: P * n(n+1)/2 * (r / (12 * 100))
    interest_earned = round(p * (n * (n + 1) / 2) * (rate / 1200), 2)
    total_principal_invested = round(p * n, 2)
    maturity_amount = total_principal_invested + interest_earned

    rd_id = f"RD-{uuid.uuid4().hex[:6].upper()}"
    maturity_date = (datetime.utcnow() + timedelta(days=n * 30)).strftime("%Y-%m-%d")

    new_rd = {
        "deposit_id": rd_id,
        "cif": debit_acc.get("cif", "CIF100001"),
        "account_number": rd_id.replace("-", ""),
        "deposit_type": "RECURRING_DEPOSIT",
        "principal_amount": p,
        "formatted_principal": f"₹{p:,.2f}/month",
        "interest_rate": rate,
        "maturity_amount": maturity_amount,
        "formatted_maturity": f"₹{maturity_amount:,.2f}",
        "deposit_date": datetime.utcnow().strftime("%Y-%m-%d"),
        "maturity_date": maturity_date,
        "tenure_months": n,
        "interest_payout_mode": "ON_MATURITY",
        "auto_renewal": False,
        "nominee_name": payload.nominee_name or "Sneha Mehta",
        "status": "ACTIVE"
    }

    mock_db.deposits.append(new_rd)
    return ApiResponse(
        data=TermDepositAccountItem(**new_rd),
        message=f"Recurring Deposit created successfully. Monthly installment of ₹{p:,.2f} scheduled on day {payload.installment_day}."
    )

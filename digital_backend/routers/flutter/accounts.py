from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional, List
from digital_backend.schemas.common import ApiResponse, BaseApiResponse
from digital_backend.schemas.flutter_schemas import (
    DashboardAccountCard,
    AccountStatementResponse,
    TransactionDetailRecord,
    AccountLimitsUpdateRequest,
    FundsInClearingItem,
    RecentTransactionItem,
    UpcomingPaymentItem
)
from digital_backend.mock_store import mock_db

router = APIRouter(tags=["4. App Accounts & Statements"])

@router.get("/accounts", response_model=ApiResponse[List[DashboardAccountCard]], summary="List All Customer Accounts")
async def list_customer_accounts(cif: str = "CIF100001"):
    """
    Returns all Savings, Current, and Operational accounts associated with the authenticated customer.
    """
    customer_accounts = [acc for acc in mock_db.accounts.values() if acc["cif"] == cif]
    cards = [
        DashboardAccountCard(
            account_id=acc["account_id"],
            account_number=acc["account_number"],
            masked_account_number=acc["masked_account_number"],
            account_type=acc["account_type"],
            account_type_code=acc["account_type_code"],
            status=acc["status"],
            available_balance=acc["available_balance"],
            formatted_balance=f"₹{acc['available_balance']:,.2f}",
            currency=acc["currency"],
            currency_symbol=acc["currency_symbol"],
            ifsc=acc["ifsc"],
            interest_rate=acc.get("interest_rate"),
            is_primary=acc["is_primary"]
        )
        for acc in customer_accounts
    ]
    return ApiResponse(data=cards, message="Accounts list fetched")


@router.get("/accounts/{account_number}", response_model=ApiResponse[dict], summary="Get Account 360 Details")
async def get_account_detail(account_number: str):
    """
    Fetch comprehensive account details including balances, IFSC, branch, nominees, and transaction limits.
    """
    acc = mock_db.accounts.get(account_number)
    if not acc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "ACCOUNT_NOT_FOUND", "message": f"Account {account_number} not found"}
        )
    return ApiResponse(data=acc, message="Account details fetched")


@router.get("/accounts/{account_number}/mini-statement", response_model=ApiResponse[List[RecentTransactionItem]], summary="Get Mini Statement")
async def get_mini_statement(account_number: str):
    """
    Returns the last 5 transactions for quick review.
    """
    txns = [RecentTransactionItem(**t) for t in mock_db.transactions[:5]]
    return ApiResponse(data=txns, message="Mini statement generated")


@router.get("/accounts/{account_number}/statement", response_model=ApiResponse[AccountStatementResponse], summary="Get Paginated Detailed Statement")
async def get_account_statement(
    account_number: str,
    from_date: Optional[str] = Query(default="2026-08-01", description="Start date YYYY-MM-DD"),
    to_date: Optional[str] = Query(default="2026-09-07", description="End date YYYY-MM-DD"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50)
):
    """
    Returns detailed transaction statement with opening/closing balances and pagination.
    """
    acc = mock_db.accounts.get(account_number, list(mock_db.accounts.values())[0])
    acc_txns = [t for t in mock_db.transactions if t.get("account_number") == account_number or account_number == "101000000012"]
    
    txns = [
        TransactionDetailRecord(
            transaction_id=t["transaction_id"],
            reference_no=t["reference_no"],
            transaction_date=t["transaction_date"],
            value_date=t["value_date"],
            narration=t["narration"],
            type=t["type"],
            amount=t["amount"],
            formatted_amount=f"-₹{t['amount']:,.2f}" if t["type"] == "DEBIT" else f"+₹{t['amount']:,.2f}",
            balance_after=t["balance_after"],
            formatted_balance_after=f"₹{t['balance_after']:,.2f}",
            channel=t["channel"],
            status="SUCCESS"
        )
        for t in acc_txns
    ]
    
    response = AccountStatementResponse(
        account_number=acc["account_number"],
        account_holder_name="Arjun Mehta",
        opening_balance=521950.00,
        closing_balance=acc["available_balance"],
        total_debits=sum([t.amount for t in txns if t.type == "DEBIT"]),
        total_credits=sum([t.amount for t in txns if t.type == "CREDIT"]),
        from_date=from_date,
        to_date=to_date,
        transactions=txns,
        total_records=len(txns),
        page=page,
        page_size=page_size
    )
    return ApiResponse(data=response, message="Statement retrieved successfully")


@router.get("/accounts/{account_number}/statement/download", response_model=ApiResponse[dict], summary="Download Statement (PDF / Excel)")
async def download_statement(
    account_number: str,
    format: str = Query(default="PDF", pattern="^(PDF|EXCEL|CSV)$"),
    from_date: Optional[str] = "2026-08-01",
    to_date: Optional[str] = "2026-09-07"
):
    """
    Generates download link for statement in PDF, Excel, or CSV format.
    """
    return ApiResponse(
        data={
            "account_number": account_number,
            "format": format,
            "file_name": f"BharatBank_Statement_{account_number}_{from_date}_{to_date}.{format.lower()}",
            "download_url": f"https://statements.bharatbank.com/download/{account_number}_{format.lower()}",
            "file_size_kb": 124.5,
            "generated_timestamp": "2026-09-07T06:30:00Z"
        },
        message="Statement download ready"
    )


@router.get("/accounts/{account_number}/limits", response_model=ApiResponse[dict], summary="Get Account Daily Transaction Limits")
async def get_account_limits(account_number: str):
    """
    Returns channel transaction limits (UPI, IMPS, NEFT/RTGS).
    """
    acc = mock_db.accounts.get(account_number, list(mock_db.accounts.values())[0])
    return ApiResponse(
        data={
            "account_number": acc["account_number"],
            "daily_upi_limit": acc.get("daily_upi_limit", 100000.00),
            "daily_imps_limit": acc.get("daily_imps_limit", 500000.00),
            "daily_neft_rtgs_limit": acc.get("daily_neft_rtgs_limit", 2000000.00),
            "international_transfers_enabled": False
        },
        message="Limits retrieved"
    )


@router.put("/accounts/{account_number}/limits", response_model=BaseApiResponse, summary="Update Account Daily Transaction Limits")
async def update_account_limits(account_number: str, payload: AccountLimitsUpdateRequest):
    """
    Adjust customer channel limits.
    """
    return BaseApiResponse(success=True, response_code="BB-200", message="Account limits updated successfully")


@router.get("/accounts/{account_number}/funds-in-clearing", response_model=ApiResponse[List[FundsInClearingItem]], summary="Inquire Funds in Clearing")
async def get_funds_in_clearing(account_number: str):
    """
    Returns uncleared cheques pending clearing house settlement.
    """
    items = [
        FundsInClearingItem(
            cheque_number="550001",
            deposit_date="2026-09-05",
            amount=25000.00,
            clearing_type="CTS (Cheque Truncation System)",
            expected_clearance_date="2026-09-08",
            status="IN_CLEARING"
        )
    ]
    return ApiResponse(data=items, message="Funds in clearing retrieved")


@router.get("/recent-transactions", response_model=ApiResponse[List[RecentTransactionItem]], summary="Get Recent Transactions (Dedicated Route)")
async def get_recent_transactions(
    limit: int = Query(default=10, ge=1, le=50),
    payment_mode: Optional[str] = Query(default=None, description="Card, UPI, NEFT, IMPS")
):
    """
    Dedicated endpoint for recent transaction activity.
    """
    txns = [RecentTransactionItem(**t) for t in mock_db.transactions]
    if payment_mode:
        txns = [t for t in txns if t.payment_mode.upper() == payment_mode.upper()]
    return ApiResponse(data=txns[:limit], message="Recent transactions fetched")


@router.get("/upcoming-payments", response_model=ApiResponse[List[UpcomingPaymentItem]], summary="Get Upcoming Payments & Dues (Dedicated Route)")
async def get_upcoming_payments(cif: str = "CIF100001"):
    """
    Dedicated endpoint for scheduled bill payments, EMIs, and dues.
    """
    items = [UpcomingPaymentItem(**up) for up in mock_db.upcoming_payments if up.get("cif") == cif]
    return ApiResponse(data=items, message="Upcoming payments retrieved")

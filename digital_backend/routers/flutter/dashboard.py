from fastapi import APIRouter
from digital_backend.schemas.common import ApiResponse
from digital_backend.schemas.flutter_schemas import (
    DashboardResponseData,
    DashboardAccountCard,
    CreditCardSummaryWidget,
    QuickActionItem,
    BankingServiceModule,
    UpcomingPaymentItem,
    RecentTransactionItem,
    PreApprovedOffer,
    PromotionalBanner
)
from digital_backend.mock_store import mock_db

router = APIRouter(tags=["3. App Dashboard"])

@router.get("/dashboard", response_model=ApiResponse[DashboardResponseData], summary="Get Customer Mobile Dashboard (Composite)")
async def get_dashboard_data():
    """
    Consolidated Mobile App Dashboard API delivering:
    - Customer details & Greeting (Arjun Mehta, Retail, Last Login)
    - Available accounts carousel (Savings & Current balances)
    - Quick Action shortcuts (Transfer, Pay Bills, Send via Mobile, Beneficiaries)
    - 16 Banking Services Grid
    - Credit Card Outstanding widget (Signature Mastercard **** 3349 due ₹67,500)
    - Recent Transactions with mode & icons (Top 5 on home dashboard)
    - Upcoming payments (Credit Card, Loan EMI, Utility Bill)
    - Pre-Approved Instant Personal Loan Offer & Banner Carousels
    """
    customer_info = mock_db.customers["CIF100001"]
    
    # Filter customer's own active accounts for the home card carousel
    customer_accounts = [acc for acc in mock_db.accounts.values() if acc["cif"] == "CIF100001"]
    account_cards = [
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

    credit_card_widgets = [
        CreditCardSummaryWidget(
            card_id=c["card_id"],
            card_title=c["card_name"],
            card_type=c["card_type"],
            masked_card_number=c["masked_card_number"],
            total_outstanding_due=c["outstanding_due"],
            formatted_outstanding_due=c["formatted_outstanding_due"],
            due_in_text=c["due_in_text"],
            due_date=c["due_date"],
            cta_text=c["cta_text"],
            is_active=True
        )
        for c in mock_db.cards if c["cif"] == "CIF100001" and c["card_type"] == "CREDIT"
    ]

    quick_actions = [QuickActionItem(**qa) for qa in mock_db.quick_actions]
    banking_services = [BankingServiceModule(**bs) for bs in mock_db.banking_services]
    upcoming_payments = [UpcomingPaymentItem(**up) for up in mock_db.upcoming_payments if up["cif"] == "CIF100001"]
    recent_transactions = [RecentTransactionItem(**rt) for rt in mock_db.transactions[:5]]
    pre_approved_offers = [PreApprovedOffer(**pao) for pao in mock_db.pre_approved_offers]
    banners = [PromotionalBanner(**b) for b in mock_db.banners]

    response_data = DashboardResponseData(
        customer={
            "cif": customer_info["cif"],
            "name": customer_info["name"],
            "segment": customer_info["customer_type"],
            "last_login": customer_info["last_login"],
            "avatar_url": customer_info["avatar_url"],
            "unread_notifications_count": 1
        },
        accounts=account_cards,
        credit_cards=credit_card_widgets,
        quick_actions=quick_actions,
        banking_services=banking_services,
        upcoming_payments=upcoming_payments,
        recent_transactions=recent_transactions,
        pre_approved_offers=pre_approved_offers,
        banners=banners
    )

    return ApiResponse(data=response_data, message="Dashboard loaded successfully")

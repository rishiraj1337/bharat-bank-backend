from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

# ==========================================================
# 1. System, Version & Theme Schemas
# ==========================================================

class SubsystemHealth(BaseModel):
    name: str = Field(..., example="CBS (Core Banking)")
    status: str = Field(..., example="UP", description="UP, DEGRADED, DOWN")
    latency_ms: float = Field(..., example=12.4)
    last_checked: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


class AppVersionResponse(BaseModel):
    app_name: str = Field(default="Bharat Bank Mobile", example="Bharat Bank Mobile")
    app_version: str = Field(default="2.4.0", example="2.4.0")
    build_number: int = Field(default=240, example=240)
    backend_version: str = Field(default="1.0.0", example="1.0.0")
    min_supported_version: str = Field(default="2.0.0", example="2.0.0")
    force_update_required: bool = Field(default=False, example=False)
    update_url_android: str = Field(default="https://play.google.com/store/apps/details?id=com.bharatbank.digital", example="https://play.google.com/store/apps/details?id=com.bharatbank.digital")
    update_url_ios: str = Field(default="https://apps.apple.com/app/bharat-bank/id123456789", example="https://apps.apple.com/app/bharat-bank/id123456789")
    server_status: str = Field(default="HEALTHY", example="HEALTHY")
    environment: str = Field(default="production-mock", example="production-mock")
    subsystems: List[SubsystemHealth] = Field(default_factory=list)


class ColorPalette(BaseModel):
    primary: str = Field(..., example="#1A56DB", description="Primary brand color (Hex)")
    secondary: str = Field(..., example="#3B82F6", description="Secondary accent color (Hex)")
    accent: str = Field(..., example="#10B981", description="Highlight/Action color (Hex)")
    background: str = Field(..., example="#F8FAFC", description="Screen background color")
    surface: str = Field(..., example="#FFFFFF", description="Card / Component surface color")
    text_primary: str = Field(..., example="#0F172A", description="Main body & title text")
    text_secondary: str = Field(..., example="#64748B", description="Subtext & muted label color")
    border: str = Field(..., example="#E2E8F0", description="Divider and border color")


class TypographyConfig(BaseModel):
    font_family_heading: str = Field(default="Inter", example="Inter")
    font_family_body: str = Field(default="Inter", example="Inter")
    heading_font_size_scale: float = Field(default=1.0, example=1.0)
    body_font_size_scale: float = Field(default=1.0, example=1.0)


class ThemeConfigResponse(BaseModel):
    theme_id: str = Field(default="bharat_bank_modern_v1", example="bharat_bank_modern_v1")
    theme_version: str = Field(default="1.2.0", example="1.2.0")
    is_dark_mode_configured: bool = Field(default=True, example=True, description="Indicates if dark mode styling is enabled")
    light_colors: ColorPalette = Field(..., description="Theme color palette for light mode")
    dark_colors: ColorPalette = Field(..., description="Theme color palette for dark mode")
    typography: TypographyConfig = Field(..., description="Font typography configuration")
    logo_url: str = Field(default="https://assets.bharatbank.com/branding/logo-standard.png", example="https://assets.bharatbank.com/branding/logo-standard.png")
    light_logo_url: str = Field(default="https://assets.bharatbank.com/branding/logo-light.png", example="https://assets.bharatbank.com/branding/logo-light.png")
    dark_logo_url: str = Field(default="https://assets.bharatbank.com/branding/logo-dark.png", example="https://assets.bharatbank.com/branding/logo-dark.png")
    favicon_url: str = Field(default="https://assets.bharatbank.com/branding/favicon.ico", example="https://assets.bharatbank.com/branding/favicon.ico")
    app_name: str = Field(default="Bharat Bank", example="Bharat Bank")
    brand_tagline: str = Field(default="Empowering Every Indian with Smart Banking", example="Empowering Every Indian with Smart Banking")


class BranchAtmItem(BaseModel):
    id: str = Field(..., example="BR-001")
    type: str = Field(..., example="BRANCH", description="BRANCH, ATM, CASH_DEPOSIT_MACHINE")
    name: str = Field(..., example="Bharat Bank - Nariman Point Branch")
    address: str = Field(..., example="102, Maker Chambers V, Nariman Point, Mumbai, Maharashtra 400021")
    city: str = Field(default="Mumbai", example="Mumbai")
    ifsc_code: Optional[str] = Field(default="APEX0001048", example="APEX0001048")
    contact_phone: Optional[str] = Field(default="+91 22 2288 9900", example="+91 22 2288 9900")
    latitude: float = Field(..., example=18.9272)
    longitude: float = Field(..., example=72.8228)
    distance_km: float = Field(default=1.2, example=1.2)
    operating_hours: str = Field(default="10:00 AM - 04:30 PM (Mon-Sat, 2nd & 4th Sat off)", example="10:00 AM - 04:30 PM")
    services_available: List[str] = Field(default=["Locker", "Cash Deposit", "Forex", "Cheque Drop Box"], example=["Locker", "Cash Deposit"])
    is_open_now: bool = Field(default=True, example=True)


# ==========================================================
# 2. Authentication & Verification Schemas
# ==========================================================

class MpinVerifyRequest(BaseModel):
    mpin: str = Field(default="1234", example="1234", min_length=4, max_length=6, description="4 or 6-digit MPIN for instant mobile login")
    cif: Optional[str] = Field(default="CIF100001", example="CIF100001")
    device_id: Optional[str] = Field(default="DEV-ANDROID-98711", example="DEV-ANDROID-98711")


class MpinSetRequest(BaseModel):
    cif: str = Field(default="CIF100001", example="CIF100001")
    old_mpin: Optional[str] = Field(default=None, example="1234")
    new_mpin: str = Field(..., example="5678", min_length=4, max_length=6)
    confirm_mpin: str = Field(..., example="5678", min_length=4, max_length=6)
    otp: Optional[str] = Field(default="123456", example="123456")


class BiometricVerifyRequest(BaseModel):
    biometric_token: str = Field(default="bio_sig_9901a88b201948ce771", example="bio_sig_9901a88b201948ce771", description="Signed hardware biometric cryptographic challenge")
    cif: Optional[str] = Field(default="CIF100001", example="CIF100001")
    device_id: Optional[str] = Field(default="DEV-ANDROID-98711", example="DEV-ANDROID-98711")


class BiometricRegisterRequest(BaseModel):
    cif: str = Field(default="CIF100001", example="CIF100001")
    public_key: str = Field(..., example="MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8...")
    device_id: str = Field(..., example="DEV-ANDROID-98711")
    device_name: str = Field(default="Google Pixel 8 Pro", example="Google Pixel 8 Pro")


class OtpSendRequest(BaseModel):
    cif: Optional[str] = Field(default="CIF100001", example="CIF100001")
    mobile_number: Optional[str] = Field(default="9876543210", example="9876543210")
    purpose: str = Field(default="LOGIN", example="LOGIN", description="LOGIN, TRANSACTION_AUTH, BENEFICIARY_ADD, MPIN_RESET")
    amount: Optional[float] = Field(default=None, example=5000.00)


class OtpVerifyRequest(BaseModel):
    otp_reference: str = Field(..., example="OTP-REF-889102")
    otp_code: str = Field(..., example="123456", min_length=4, max_length=6)
    cif: Optional[str] = Field(default="CIF100001", example="CIF100001")


class CustomerLoginRequest(BaseModel):
    mpin: Optional[str] = Field(default="1234", example="1234", description="4-digit MPIN for quick mobile login")
    login_id: Optional[str] = Field(default="arjun.mehta", example="arjun.mehta", description="Optional username/CIF if logging in with credentials")
    password: Optional[str] = Field(default=None, example=None, description="Only required if using internet banking password login instead of MPIN")
    device_id: Optional[str] = Field(default="DEV-ANDROID-98711", example="DEV-ANDROID-98711")


class CustomerRegisterRequest(BaseModel):
    cif: str = Field(..., example="CIF100001")
    account_number: str = Field(..., example="101000000001")
    mobile_number: str = Field(..., example="9876543210")
    email: str = Field(..., example="arjun.mehta@bharatbank.com")
    pan_number: str = Field(..., example="ABCDE1234F")
    date_of_birth: str = Field(..., example="1992-05-14")
    desired_login_id: str = Field(..., example="arjun.mehta")
    mpin: str = Field(..., example="1234")


class AuthSessionData(BaseModel):
    cif: str = Field(..., example="CIF100001")
    customer_name: str = Field(..., example="Arjun Mehta")
    customer_type: str = Field(default="RETAIL", example="RETAIL")
    email: str = Field(default="arjun.mehta@bharatbank.com", example="arjun.mehta@bharatbank.com")
    mobile_number: str = Field(default="9876543210", example="9876543210")
    last_login_at: str = Field(default="Today, 09:42 AM", example="Today, 09:42 AM")
    access_token: str = Field(default="mock_jwt_token_retail_arjun_mehta", example="mock_jwt_token_retail_arjun_mehta")
    token_type: str = Field(default="Bearer", example="Bearer")
    expires_in_seconds: int = Field(default=86400, example=86400)


# ==========================================================
# 3. Dashboard Composite Schemas (Exact UI Match)
# ==========================================================

class DashboardAccountCard(BaseModel):
    account_id: str = Field(..., example="ACC-101000000012")
    account_number: str = Field(..., example="101000000012")
    masked_account_number: str = Field(..., example="**** **** 0012")
    account_type: str = Field(..., example="Savings Account", description="Savings Account, Current Account, Fixed Deposit")
    account_type_code: str = Field(default="SAVINGS", example="SAVINGS")
    status: str = Field(default="Active", example="Active")
    available_balance: float = Field(..., example=482450.00)
    formatted_balance: str = Field(..., example="₹4,82,450.00")
    currency: str = Field(default="INR", example="INR")
    currency_symbol: str = Field(default="₹", example="₹")
    ifsc: str = Field(default="APEX0001048", example="APEX0001048")
    interest_rate: Optional[str] = Field(default="6.5% p.a.", example="6.5% p.a.")
    is_primary: bool = Field(default=True, example=True)


class QuickActionItem(BaseModel):
    id: str = Field(..., example="qa_transfer")
    title: str = Field(..., example="Transfer")
    icon: str = Field(..., example="transfer_arrows")
    route: str = Field(..., example="/transfers")
    category: str = Field(default="PAYMENT", example="PAYMENT")
    badge: Optional[str] = Field(default="Instant (24/7)", example="Instant (24/7)")


class BankingServiceModule(BaseModel):
    id: str = Field(..., example="srv_accounts")
    title: str = Field(..., example="Accounts")
    icon: str = Field(..., example="wallet")
    route: str = Field(..., example="/accounts")
    category: str = Field(default="CORE", example="CORE")
    badge: Optional[str] = None


class CreditCardSummaryWidget(BaseModel):
    card_id: str = Field(default="CRD-3349", example="CRD-3349")
    card_title: str = Field(default="Signature Mastercard", example="Signature Mastercard")
    card_type: str = Field(default="CREDIT", example="CREDIT")
    masked_card_number: str = Field(default="**** **** **** 3349", example="**** **** **** 3349")
    total_outstanding_due: float = Field(default=67500.00, example=67500.00)
    formatted_outstanding_due: str = Field(default="₹67,500", example="₹67,500")
    due_in_text: str = Field(default="Due in 11 days", example="Due in 11 days")
    due_date: str = Field(default="2026-09-18", example="2026-09-18")
    cta_text: str = Field(default="Pay Card Bill", example="Pay Card Bill")
    is_active: bool = Field(default=True, example=True)


class RecentTransactionItem(BaseModel):
    transaction_id: str = Field(..., example="TXN-20260907-001")
    title: str = Field(..., example="Apple Store Mumbai BKC")
    subtitle: str = Field(..., example="Today, 10:14 AM • Card")
    date_formatted: str = Field(..., example="Today, 10:14 AM")
    payment_mode: str = Field(..., example="Card", description="Card, UPI, NEFT, IMPS, RTGS, NACH")
    amount: float = Field(..., example=14500.00)
    formatted_amount: str = Field(..., example="-₹14,500")
    type: str = Field(..., example="DEBIT", description="DEBIT or CREDIT")
    status: str = Field(default="Success", example="Success")
    category: str = Field(default="Shopping", example="Shopping")
    icon: Optional[str] = Field(default="arrow_outward", example="arrow_outward")


class UpcomingPaymentItem(BaseModel):
    id: str = Field(..., example="UPAY-001")
    title: str = Field(..., example="Signature Mastercard Bill")
    biller_or_payee: str = Field(..., example="Bharat Bank Credit Cards")
    amount: float = Field(..., example=67500.00)
    formatted_amount: str = Field(..., example="₹67,500.00")
    due_date: str = Field(..., example="2026-09-18")
    due_in_days: int = Field(..., example=11)
    type: str = Field(..., example="CREDIT_CARD", description="CREDIT_CARD, LOAN_EMI, UTILITY_BILL, SIP")
    is_autopay_enabled: bool = Field(default=False, example=False)


class PreApprovedOffer(BaseModel):
    id: str = Field(default="OFFER-PL-500K", example="OFFER-PL-500K")
    badge: str = Field(default="PRE-APPROVED OFFER", example="PRE-APPROVED OFFER")
    title: str = Field(default="Instant Personal Loan up to ₹5,00,000", example="Instant Personal Loan up to ₹5,00,000")
    subtitle: str = Field(default="Disbursed in 30 seconds with zero paperwork.", example="Disbursed in 30 seconds with zero paperwork.")
    cta_text: str = Field(default="Avail Now", example="Avail Now")
    cta_route: str = Field(default="/loans/pre-approved/apply", example="/loans/pre-approved/apply")
    max_amount: float = Field(default=500000.00, example=500000.00)
    interest_rate_p_a: float = Field(default=10.49, example=10.49)
    valid_until: str = Field(default="2026-09-30", example="2026-09-30")


class PromotionalBanner(BaseModel):
    id: str = Field(..., example="BANNER-01")
    image_url: str = Field(..., example="https://assets.bharatbank.com/banners/fixed-deposit-fest.png")
    title: str = Field(..., example="Special Monsoon FD Rates at 7.75% p.a.")
    deeplink: str = Field(..., example="/deposits/open-fd")


class DashboardResponseData(BaseModel):
    customer: Dict[str, Any] = Field(..., example={
        "cif": "CIF100001",
        "name": "Arjun Mehta",
        "segment": "RETAIL",
        "last_login": "Today, 09:42 AM",
        "avatar_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150",
        "unread_notifications_count": 1
    })
    accounts: List[DashboardAccountCard]
    credit_cards: List[CreditCardSummaryWidget]
    quick_actions: List[QuickActionItem]
    banking_services: List[BankingServiceModule]
    upcoming_payments: List[UpcomingPaymentItem]
    recent_transactions: List[RecentTransactionItem]
    pre_approved_offers: List[PreApprovedOffer]
    banners: List[PromotionalBanner]


# ==========================================================
# 4. Accounts & Statements Schemas
# ==========================================================

class AccountStatementFilter(BaseModel):
    account_number: str = Field(..., example="101000000012")
    from_date: Optional[str] = Field(default="2026-08-01", example="2026-08-01")
    to_date: Optional[str] = Field(default="2026-09-07", example="2026-09-07")
    txn_type: Optional[str] = Field(default=None, example="ALL", description="ALL, DEBIT, CREDIT")
    page: int = Field(default=1, example=1)
    page_size: int = Field(default=10, example=10)


class TransactionDetailRecord(BaseModel):
    transaction_id: str = Field(..., example="TXN-20260907-001")
    reference_no: str = Field(..., example="REF99281023")
    transaction_date: str = Field(..., example="2026-09-07")
    value_date: str = Field(..., example="2026-09-07")
    narration: str = Field(..., example="Apple Store Mumbai BKC - POS Purchase")
    type: str = Field(..., example="DEBIT", description="DEBIT or CREDIT")
    amount: float = Field(..., example=14500.00)
    formatted_amount: str = Field(..., example="-₹14,500.00")
    balance_after: float = Field(..., example=482450.00)
    formatted_balance_after: str = Field(..., example="₹4,82,450.00")
    channel: str = Field(default="CARD", example="CARD")
    status: str = Field(default="SUCCESS", example="SUCCESS")


class AccountStatementResponse(BaseModel):
    account_number: str = Field(..., example="101000000012")
    account_holder_name: str = Field(..., example="Arjun Mehta")
    opening_balance: float = Field(..., example=521950.00)
    closing_balance: float = Field(..., example=482450.00)
    total_debits: float = Field(..., example=44500.00)
    total_credits: float = Field(..., example=5000.00)
    from_date: str = Field(..., example="2026-08-01")
    to_date: str = Field(..., example="2026-09-07")
    transactions: List[TransactionDetailRecord]
    total_records: int = Field(..., example=15)
    page: int = Field(..., example=1)
    page_size: int = Field(..., example=10)


class AccountLimitsUpdateRequest(BaseModel):
    daily_upi_limit: Optional[float] = Field(default=100000.00, example=100000.00)
    daily_imps_limit: Optional[float] = Field(default=500000.00, example=500000.00)
    daily_neft_rtgs_limit: Optional[float] = Field(default=2000000.00, example=2000000.00)
    international_transfers_enabled: Optional[bool] = Field(default=False, example=False)


class FundsInClearingItem(BaseModel):
    cheque_number: str = Field(..., example="550001")
    deposit_date: str = Field(..., example="2026-09-05")
    amount: float = Field(..., example=25000.00)
    clearing_type: str = Field(default="CTS", example="CTS")
    expected_clearance_date: str = Field(..., example="2026-09-08")
    status: str = Field(default="IN_CLEARING", example="IN_CLEARING")


# ==========================================================
# 5. Transfers & Beneficiaries Schemas (Screenshots 2, 3, 4)
# ==========================================================

class TransferTypeOption(BaseModel):
    code: str = Field(..., example="IMPS", description="WITHIN_BANK, IMPS, NEFT, RTGS")
    title: str = Field(..., example="IMPS")
    subtitle: str = Field(..., example="Instant transfer 24x7 · up to ₹5 lakh")
    icon: str = Field(..., example="bolt")
    min_amount: float = Field(default=1.0, example=1.0)
    max_amount: float = Field(default=500000.0, example=500000.0)
    charge: float = Field(default=0.0, example=0.0)
    settlement_type: str = Field(default="Instant 24x7", example="Instant 24x7")


class BeneficiaryItem(BaseModel):
    beneficiary_id: str = Field(..., example="BEN-001")
    name: str = Field(..., example="Sneha Mehta")
    bank_name: str = Field(..., example="Bharat Co-operative Bank")
    account_number: str = Field(..., example="99182390129182")
    masked_account_number: str = Field(..., example="**** **** 9182")
    ifsc: str = Field(default="BCOB0001234", example="BCOB0001234")
    account_type: str = Field(default="SAVINGS", example="SAVINGS")
    transfer_type: str = Field(default="IMPS", example="IMPS", description="WITHIN_BANK, IMPS, NEFT, RTGS")
    avatar_initials: str = Field(default="SM", example="SM")
    is_within_bank: bool = Field(default=False, example=False)
    cooling_period_active: bool = Field(default=False, example=False)
    max_transfer_limit: float = Field(default=500000.00, example=500000.00)


class AddBeneficiaryRequest(BaseModel):
    name: str = Field(..., example="Sneha Mehta")
    account_number: str = Field(..., example="99182390129182")
    confirm_account_number: str = Field(..., example="99182390129182")
    ifsc: str = Field(..., example="BCOB0001234")
    bank_name: Optional[str] = Field(default="Bharat Co-operative Bank", example="Bharat Co-operative Bank")
    account_type: Optional[str] = Field(default="SAVINGS", example="SAVINGS")
    nickname: Optional[str] = Field(default="Sneha Personal", example="Sneha Personal")
    otp: Optional[str] = Field(default="123456", example="123456")


class TransferInitiateRequest(BaseModel):
    debit_account_number: str = Field(..., example="101000000012", description="Funding Account")
    beneficiary_id: Optional[str] = Field(default=None, example="BEN-001")
    beneficiary_name: str = Field(..., example="Sneha Mehta")
    beneficiary_account_number: str = Field(..., example="99182390129182")
    beneficiary_ifsc: Optional[str] = Field(default="BCOB0001234", example="BCOB0001234")
    beneficiary_bank_name: Optional[str] = Field(default="Bharat Co-operative Bank", example="Bharat Co-operative Bank")
    amount: float = Field(..., example=5000.00)
    transfer_type: str = Field(default="IMPS", example="IMPS", description="WITHIN_BANK, IMPS, NEFT, RTGS")
    note: Optional[str] = Field(default="Payment note", example="Payment note")
    mpin: Optional[str] = Field(default="1234", example="1234")


class TransferInitiateResponse(BaseModel):
    transaction_id: str = Field(..., example="TXN-20260907-88912")
    utr: str = Field(..., example="UTR-IMPS-20260907-99120")
    reference_no: str = Field(..., example="REF88392109")
    status: str = Field(default="SUCCESS", example="SUCCESS", description="SUCCESS, PENDING, FAILED")
    amount: float = Field(..., example=5000.00)
    formatted_amount: str = Field(..., example="₹5,000.00")
    fee: float = Field(default=0.00, example=0.00)
    debit_account_number: str = Field(..., example="101000000012")
    receiver_name: str = Field(..., example="Sneha Mehta")
    receiver_bank: str = Field(..., example="Bharat Co-operative Bank")
    receiver_masked_account: str = Field(..., example="**** **** 9182")
    transfer_type: str = Field(..., example="IMPS")
    note: Optional[str] = Field(default="Payment note", example="Payment note")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    balance_remaining: float = Field(default=477450.00, example=477450.00)


class ScheduleTransferRequest(BaseModel):
    debit_account_number: str = Field(..., example="101000000012")
    beneficiary_name: str = Field(..., example="Sneha Mehta")
    beneficiary_account_number: str = Field(..., example="99182390129182")
    beneficiary_ifsc: str = Field(..., example="BCOB0001234")
    amount: float = Field(..., example=5000.00)
    frequency: str = Field(default="MONTHLY", example="MONTHLY", description="ONCE, DAILY, WEEKLY, MONTHLY")
    start_date: str = Field(..., example="2026-10-01")
    end_date: Optional[str] = Field(default="2027-10-01", example="2027-10-01")
    installments: Optional[int] = Field(default=12, example=12)
    transfer_type: str = Field(default="IMPS", example="IMPS")


class IfscLookupResponse(BaseModel):
    ifsc: str = Field(..., example="APEX0001048")
    bank_name: str = Field(..., example="Bharat Bank")
    branch_name: str = Field(..., example="Nariman Point Branch")
    address: str = Field(..., example="102, Maker Chambers V, Nariman Point, Mumbai")
    city: str = Field(..., example="Mumbai")
    state: str = Field(..., example="Maharashtra")
    rtgs_supported: bool = Field(default=True, example=True)
    neft_supported: bool = Field(default=True, example=True)
    imps_supported: bool = Field(default=True, example=True)
    micr: str = Field(default="400002001", example="400002001")


# ==========================================================
# 6. Cards Schemas (Credit & Debit)
# ==========================================================

class CardDetailItem(BaseModel):
    card_id: str = Field(..., example="CRD-3349")
    card_number: str = Field(..., example="5412750012343349")
    masked_card_number: str = Field(..., example="**** **** **** 3349")
    card_holder_name: str = Field(..., example="Arjun Mehta")
    card_type: str = Field(..., example="CREDIT", description="CREDIT or DEBIT")
    card_network: str = Field(..., example="Mastercard", description="Mastercard, Visa, RuPay")
    card_name: str = Field(..., example="Signature Mastercard")
    expiry_date: str = Field(..., example="12/29")
    cvv: str = Field(default="***", example="***")
    is_locked: bool = Field(default=False, example=False)
    is_blocked: bool = Field(default=False, example=False)
    credit_limit: Optional[float] = Field(default=200000.00, example=200000.00)
    available_credit_limit: Optional[float] = Field(default=132500.00, example=132500.00)
    outstanding_due: Optional[float] = Field(default=67500.00, example=67500.00)
    due_date: Optional[str] = Field(default="2026-09-18", example="2026-09-18")
    domestic_pos_enabled: bool = Field(default=True, example=True)
    domestic_online_enabled: bool = Field(default=True, example=True)
    international_enabled: bool = Field(default=False, example=False)
    contactless_enabled: bool = Field(default=True, example=True)


class CardLockToggleRequest(BaseModel):
    is_locked: bool = Field(..., example=True)
    reason: Optional[str] = Field(default="USER_APP_TOGGLE", example="USER_APP_TOGGLE")


class CardBlockRequest(BaseModel):
    reason: str = Field(..., example="LOST_OR_STOLEN", description="LOST_OR_STOLEN, SUSPECTED_FRAUD, DAMAGED")
    reissue_requested: bool = Field(default=True, example=True)
    delivery_address: Optional[str] = Field(default="102, Palm Heights, Bandra West, Mumbai", example="102, Palm Heights, Bandra West, Mumbai")


class CardBillPaymentRequest(BaseModel):
    debit_account_number: str = Field(..., example="101000000012")
    amount: float = Field(..., example=67500.00)
    payment_option: str = Field(default="TOTAL_DUE", example="TOTAL_DUE", description="TOTAL_DUE, MINIMUM_DUE, CUSTOM_AMOUNT")


# ==========================================================
# 7. Term Deposits Schemas (FD & RD)
# ==========================================================

class TermDepositAccountItem(BaseModel):
    deposit_id: str = Field(..., example="FD-1010000091")
    account_number: str = Field(..., example="FD1010000091")
    deposit_type: str = Field(..., example="FIXED_DEPOSIT", description="FIXED_DEPOSIT or RECURRING_DEPOSIT")
    principal_amount: float = Field(..., example=200000.00)
    formatted_principal: str = Field(..., example="₹2,00,000.00")
    interest_rate: float = Field(..., example=7.25)
    maturity_amount: float = Field(..., example=231800.00)
    formatted_maturity: str = Field(..., example="₹2,31,800.00")
    deposit_date: str = Field(..., example="2025-09-07")
    maturity_date: str = Field(..., example="2027-09-07")
    tenure_months: int = Field(..., example=24)
    interest_payout_mode: str = Field(default="ON_MATURITY", example="ON_MATURITY")
    auto_renewal: bool = Field(default=True, example=True)
    nominee_name: str = Field(default="Sneha Mehta", example="Sneha Mehta")
    status: str = Field(default="ACTIVE", example="ACTIVE")


class TermDepositRateItem(BaseModel):
    tenure_min_days: int = Field(..., example=365)
    tenure_max_days: int = Field(..., example=730)
    tenure_label: str = Field(..., example="1 Year to 2 Years")
    general_interest_rate: float = Field(..., example=7.25)
    senior_citizen_interest_rate: float = Field(..., example=7.75)


class TermDepositCalculateRequest(BaseModel):
    deposit_type: str = Field(default="FIXED_DEPOSIT", example="FIXED_DEPOSIT")
    amount: float = Field(..., example=100000.00)
    tenure_months: int = Field(..., example=12)
    is_senior_citizen: bool = Field(default=False, example=False)
    payout_frequency: str = Field(default="ON_MATURITY", example="ON_MATURITY")


class TermDepositCalculateResponse(BaseModel):
    principal_amount: float = Field(..., example=100000.00)
    tenure_months: int = Field(..., example=12)
    interest_rate: float = Field(..., example=7.10)
    interest_earned: float = Field(..., example=7290.00)
    maturity_amount: float = Field(..., example=107290.00)
    maturity_date: str = Field(..., example="2027-09-07")


class OpenDepositRequest(BaseModel):
    debit_account_number: str = Field(..., example="101000000012")
    deposit_type: str = Field(default="FIXED_DEPOSIT", example="FIXED_DEPOSIT")
    amount: float = Field(..., example=100000.00)
    tenure_months: int = Field(..., example=12)
    interest_payout: str = Field(default="ON_MATURITY", example="ON_MATURITY")
    auto_renewal: bool = Field(default=True, example=True)
    nominee_name: Optional[str] = Field(default="Sneha Mehta", example="Sneha Mehta")


# ==========================================================
# 8. Loans Schemas
# ==========================================================

class LoanAccountItem(BaseModel):
    loan_id: str = Field(..., example="LN-101000001")
    loan_account_number: str = Field(..., example="LN101000001")
    loan_type: str = Field(..., example="HOME_LOAN", description="HOME_LOAN, PERSONAL_LOAN, AUTO_LOAN, EDUCATION_LOAN")
    sanctioned_amount: float = Field(..., example=5000000.00)
    formatted_sanctioned: str = Field(..., example="₹50,00,000.00")
    outstanding_principal: float = Field(..., example=4250000.00)
    formatted_outstanding: str = Field(..., example="₹42,50,000.00")
    interest_rate: float = Field(..., example=8.50)
    emi_amount: float = Field(..., example=43391.00)
    formatted_emi: str = Field(..., example="₹43,391.00")
    next_due_date: str = Field(..., example="2026-09-10")
    total_tenure_months: int = Field(..., example=240)
    remaining_tenure_months: int = Field(..., example=195)
    auto_pay_linked_account: Optional[str] = Field(default="101000000012", example="101000000012")
    is_auto_pay_active: bool = Field(default=True, example=True)
    status: str = Field(default="ACTIVE", example="ACTIVE")


class RepaymentScheduleItem(BaseModel):
    installment_no: int = Field(..., example=1)
    due_date: str = Field(..., example="2026-09-10")
    principal_component: float = Field(..., example=13308.00)
    interest_component: float = Field(..., example=30083.00)
    total_installment: float = Field(..., example=43391.00)
    ending_balance: float = Field(..., example=4236692.00)
    status: str = Field(default="UPCOMING", example="UPCOMING", description="PAID, UPCOMING, OVERDUE")


class StandingInstructionRequest(BaseModel):
    loan_id: str = Field(..., example="LN-101000001")
    debit_account_number: str = Field(..., example="101000000012")
    debit_day_of_month: int = Field(default=10, example=10)
    otp: Optional[str] = Field(default="123456", example="123456")


class LoanApplicationRequest(BaseModel):
    loan_type: str = Field(default="PERSONAL_LOAN", example="PERSONAL_LOAN")
    requested_amount: float = Field(..., example=300000.00)
    tenure_months: int = Field(..., example=36)
    purpose: str = Field(default="Home Renovation", example="Home Renovation")
    monthly_income: float = Field(..., example=150000.00)
    employment_type: str = Field(default="SALARIED", example="SALARIED")


# ==========================================================
# 9. Bill Payments & BBPS Schemas
# ==========================================================

class BillerCategoryItem(BaseModel):
    category_id: str = Field(..., example="ELECTRICITY")
    category_name: str = Field(..., example="Electricity")
    icon: str = Field(..., example="flash_on")
    is_bbps_supported: bool = Field(default=True, example=True)


class BillerItem(BaseModel):
    biller_id: str = Field(..., example="BLR-ADANI-MUM")
    biller_name: str = Field(..., example="Adani Electricity Mumbai Limited")
    category_id: str = Field(..., example="ELECTRICITY")
    consumer_param_name: str = Field(default="Consumer Number (10 Digits)", example="Consumer Number (10 Digits)")
    sample_param_value: str = Field(default="1029384756", example="1029384756")
    logo_url: str = Field(default="https://assets.bharatbank.com/billers/adani.png", example="https://assets.bharatbank.com/billers/adani.png")


class FetchBillRequest(BaseModel):
    biller_id: str = Field(..., example="BLR-ADANI-MUM")
    consumer_number: str = Field(..., example="1029384756")


class FetchBillResponse(BaseModel):
    biller_id: str = Field(..., example="BLR-ADANI-MUM")
    biller_name: str = Field(..., example="Adani Electricity Mumbai Limited")
    consumer_number: str = Field(..., example="1029384756")
    customer_name: str = Field(..., example="Arjun Mehta")
    bill_number: str = Field(..., example="BILL-202609-88192")
    bill_date: str = Field(..., example="2026-09-01")
    due_date: str = Field(..., example="2026-09-20")
    bill_amount: float = Field(..., example=4500.00)
    formatted_amount: str = Field(..., example="₹4,500.00")
    is_bill_paid: bool = Field(default=False, example=False)


class PayBillRequest(BaseModel):
    biller_id: str = Field(..., example="BLR-ADANI-MUM")
    consumer_number: str = Field(..., example="1029384756")
    bill_number: Optional[str] = Field(default="BILL-202609-88192", example="BILL-202609-88192")
    debit_account_number: str = Field(..., example="101000000012")
    amount: float = Field(..., example=4500.00)
    mpin: Optional[str] = Field(default="1234", example="1234")


# ==========================================================
# 10. Cheques & Other Services Schemas
# ==========================================================

class ChequeBookRequest(BaseModel):
    account_number: str = Field(..., example="101000000012")
    number_of_leaves: int = Field(default=25, example=25, description="25, 50, or 100 leaves")
    delivery_address: Optional[str] = Field(default="Registered Communication Address", example="Registered Communication Address")


class StopChequeRequest(BaseModel):
    account_number: str = Field(..., example="101000000012")
    cheque_number: str = Field(..., example="110003")
    reason: str = Field(default="CHEQUE_LOST", example="CHEQUE_LOST", description="CHEQUE_LOST, DISPUTE, INCORRECT_AMOUNT")


class NomineeDetail(BaseModel):
    name: str = Field(..., example="Sneha Mehta")
    relation: str = Field(..., example="SPOUSE")
    date_of_birth: str = Field(default="1994-08-22", example="1994-08-22")
    share_percentage: int = Field(default=100, example=100)
    guardian_name: Optional[str] = None
    address: str = Field(default="102, Palm Heights, Bandra West, Mumbai 400050", example="102, Palm Heights, Bandra West, Mumbai 400050")


class NachMandateItem(BaseModel):
    mandate_id: str = Field(..., example="UMRN-NACH-8829104")
    beneficiary_corporate: str = Field(..., example="HDFC Life Insurance Co.")
    debit_account_number: str = Field(..., example="101000000012")
    max_amount: float = Field(..., example=25000.00)
    frequency: str = Field(default="MONTHLY", example="MONTHLY")
    start_date: str = Field(..., example="2025-01-01")
    end_date: str = Field(..., example="2035-01-01")
    status: str = Field(default="ACTIVE", example="ACTIVE")

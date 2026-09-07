from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from digital_backend.schemas.flutter_schemas import ColorPalette, TypographyConfig

# ==========================================================
# 1. Admin Users, Roles & Permissions (US-20)
# ==========================================================

class AdminUserItem(BaseModel):
    user_id: str = Field(..., example="ADM-101")
    username: str = Field(..., example="rajesh.amin")
    full_name: str = Field(..., example="Rajesh Amin")
    email: str = Field(..., example="rajesh.amin@bharatbank.com")
    role: str = Field(..., example="SUPER_ADMIN", description="SUPER_ADMIN, OPS_MAKER, OPS_CHECKER, COMPLIANCE_OFFICER, BRANCH_MANAGER")
    department: str = Field(default="IT Operations", example="IT Operations")
    branch_code: str = Field(default="001", example="001")
    is_active: bool = Field(default=True, example=True)
    last_login_at: str = Field(default="2026-09-07T05:30:00Z", example="2026-09-07T05:30:00Z")
    created_at: str = Field(default="2026-01-10T10:00:00Z", example="2026-01-10T10:00:00Z")


class AdminUserCreateRequest(BaseModel):
    username: str = Field(..., example="priya.sharma")
    full_name: str = Field(..., example="Priya Sharma")
    email: str = Field(..., example="priya.sharma@bharatbank.com")
    role: str = Field(default="OPS_CHECKER", example="OPS_CHECKER")
    department: str = Field(default="Operations", example="Operations")
    branch_code: str = Field(default="001", example="001")


class AdminRoleItem(BaseModel):
    role_id: str = Field(..., example="ROLE_SUPER_ADMIN")
    role_name: str = Field(..., example="Super Administrator")
    description: str = Field(..., example="Full unrestricted access to system configurations, admin users, and audit logs")
    permissions: List[str] = Field(default_factory=list, example=["USERS_MANAGE", "CIF_LINK", "RULES_CONFIG", "REPORTS_EXPORT", "OVERRIDE_TXN"])


# ==========================================================
# 2. Customer & CIF Management (US-21, US-02)
# ==========================================================

class AdminCustomerSummary(BaseModel):
    cif: str = Field(..., example="CIF100001")
    customer_name: str = Field(..., example="Arjun Mehta")
    customer_type: str = Field(..., example="RETAIL", description="RETAIL, CORPORATE, NRI")
    mobile_number: str = Field(..., example="9876543210")
    email: str = Field(..., example="arjun.mehta@bharatbank.com")
    pan_number: str = Field(..., example="ABCDE1234F")
    kyc_status: str = Field(..., example="VERIFIED", description="VERIFIED, PENDING, EXPIRED")
    digital_profile_status: str = Field(..., example="ACTIVE", description="ACTIVE, BLOCKED, DORMANT, NOT_ONBOARDED")
    total_accounts: int = Field(default=2, example=2)
    total_balance: float = Field(default=1677450.00, example=1677450.00)
    created_at: str = Field(default="2024-01-15", example="2024-01-15")


class AdminCustomer360Detail(BaseModel):
    cif: str = Field(..., example="CIF100001")
    customer_name: str = Field(..., example="Arjun Mehta")
    customer_type: str = Field(default="RETAIL", example="RETAIL")
    dob_or_incorporation: str = Field(default="1992-05-14", example="1992-05-14")
    gender: str = Field(default="MALE", example="MALE")
    mobile_number: str = Field(default="9876543210", example="9876543210")
    email: str = Field(default="arjun.mehta@bharatbank.com", example="arjun.mehta@bharatbank.com")
    pan_number: str = Field(default="ABCDE1234F", example="ABCDE1234F")
    aadhaar_masked: str = Field(default="XXXX-XXXX-9182", example="XXXX-XXXX-9182")
    address: str = Field(default="102, Palm Heights, Bandra West, Mumbai 400050", example="102, Palm Heights, Bandra West, Mumbai 400050")
    kyc_status: str = Field(default="VERIFIED", example="VERIFIED")
    kyc_verified_on: str = Field(default="2024-01-16", example="2024-01-16")
    digital_profile_linked: bool = Field(default=True, example=True)
    digital_status: str = Field(default="ACTIVE", example="ACTIVE")
    risk_rating: str = Field(default="LOW", example="LOW")
    home_branch: str = Field(default="Nariman Point (001)", example="Nariman Point (001)")
    accounts: List[Dict[str, Any]] = Field(default_factory=list)
    cards: List[Dict[str, Any]] = Field(default_factory=list)
    loans: List[Dict[str, Any]] = Field(default_factory=list)
    deposits: List[Dict[str, Any]] = Field(default_factory=list)


class AdminCustomerOnboardRequest(BaseModel):
    cif: str = Field(..., example="CIF100003")
    customer_name: str = Field(..., example="Vikramaditya Rao")
    customer_type: str = Field(default="RETAIL", example="RETAIL")
    mobile_number: str = Field(..., example="9811223344")
    email: str = Field(..., example="vikram.rao@gmail.com")
    pan_number: str = Field(..., example="XYZPK9918M")
    date_of_birth: str = Field(..., example="1988-11-20")
    primary_account_type: str = Field(default="SAVINGS", example="SAVINGS")
    initial_deposit_amount: float = Field(default=50000.00, example=50000.00)
    branch_code: str = Field(default="001", example="001")


class AdminCifLinkageRequest(BaseModel):
    cif: str = Field(..., example="CIF100001")
    mobile_user_id: str = Field(..., example="arjun.mehta")
    action: str = Field(default="LINK", example="LINK", description="LINK or UNLINK")
    reason: Optional[str] = Field(default="Branch assisted KYC verification completed", example="Branch assisted KYC verification")


class AdminCustomerStatusUpdateRequest(BaseModel):
    cif: str = Field(..., example="CIF100001")
    new_status: str = Field(..., example="BLOCKED", description="ACTIVE, BLOCKED, FROZEN, SUSPENDED")
    reason: str = Field(..., example="Suspected fraud investigation")


# ==========================================================
# 3. Authorization Rules & Corporate Hierarchies (US-22, US-03)
# ==========================================================

class AuthorizationRuleItem(BaseModel):
    rule_id: str = Field(..., example="RULE-CORP-TXN-01")
    rule_name: str = Field(..., example="Corporate Payment Maker-Checker Tier 1")
    client_segment: str = Field(default="CORPORATE", example="CORPORATE")
    min_amount: float = Field(..., example=100000.00)
    max_amount: float = Field(..., example=1000000.00)
    maker_role_required: str = Field(default="CORP_MAKER", example="CORP_MAKER")
    checker_role_required: str = Field(default="CORP_CHECKER_L1", example="CORP_CHECKER_L1")
    required_approvals_count: int = Field(default=1, example=1)
    cooling_period_hours: int = Field(default=2, example=2)
    is_active: bool = Field(default=True, example=True)
    version: int = Field(default=2, example=2)
    updated_by: str = Field(default="rajesh.amin", example="rajesh.amin")
    updated_at: str = Field(default="2026-08-30T14:20:00Z", example="2026-08-30T14:20:00Z")


class CreateAuthRuleRequest(BaseModel):
    rule_name: str = Field(..., example="High Value Transfer Dual-Approval")
    client_segment: str = Field(default="CORPORATE", example="CORPORATE")
    min_amount: float = Field(..., example=1000000.00)
    max_amount: float = Field(..., example=10000000.00)
    maker_role_required: str = Field(default="CORP_MAKER", example="CORP_MAKER")
    checker_role_required: str = Field(default="CORP_CHECKER_L2", example="CORP_CHECKER_L2")
    required_approvals_count: int = Field(default=2, example=2)
    cooling_period_hours: int = Field(default=4, example=4)


class CorporateHierarchyNode(BaseModel):
    hierarchy_id: str = Field(..., example="CORP-HIER-01")
    corporate_cif: str = Field(..., example="CIF-CORP-9001")
    corporate_name: str = Field(..., example="Nexus Tech Enterprises Pvt Ltd")
    login_id: str = Field(..., example="nexus.cfo")
    employee_name: str = Field(..., example="Vikram Sengupta")
    tier_level: int = Field(..., example=1, description="1=Approver/CFO, 2=Manager/Checker, 3=Staff/Maker")
    daily_limit: float = Field(..., example=10000000.00)
    per_txn_limit: float = Field(..., example=2500000.00)
    can_initiate: bool = Field(default=True, example=True)
    can_approve: bool = Field(default=True, example=True)
    status: str = Field(default="ACTIVE", example="ACTIVE")


# ==========================================================
# 4. Operations, Service Requests & Health
# ==========================================================

class AdminTransactionMonitorItem(BaseModel):
    txn_id: str = Field(..., example="TXN-20260907-88912")
    utr: str = Field(..., example="UTR-IMPS-20260907-99120")
    channel: str = Field(..., example="MOBILE_APP")
    payment_mode: str = Field(..., example="IMPS", description="IMPS, NEFT, RTGS, WITHIN_BANK, BBPS")
    sender_cif: str = Field(..., example="CIF100001")
    sender_name: str = Field(..., example="Arjun Mehta")
    sender_account: str = Field(..., example="101000000012")
    receiver_name: str = Field(..., example="Sneha Mehta")
    receiver_account: str = Field(..., example="99182390129182")
    receiver_bank: str = Field(..., example="Bharat Co-operative Bank")
    amount: float = Field(..., example=5000.00)
    status: str = Field(..., example="SUCCESS", description="SUCCESS, PENDING, FAILED, SUSPECTED_FRAUD")
    created_at: str = Field(..., example="2026-09-07T06:15:00Z")
    switch_response_code: str = Field(default="00", example="00")
    risk_score: int = Field(default=12, example=12, description="Fraud risk score 0-100")


class StatusOverrideRequest(BaseModel):
    new_status: str = Field(..., example="FORCE_SUCCESS", description="FORCE_SUCCESS, FORCE_FAIL, RECONCILED")
    reason: str = Field(..., example="Bank switch confirmed settlement after timeout")
    approver_remarks: str = Field(..., example="Verified against NPCI settlement file")


class ServiceRequestItem(BaseModel):
    request_id: str = Field(..., example="SR-202609-0012")
    cif: str = Field(..., example="CIF100001")
    customer_name: str = Field(..., example="Arjun Mehta")
    request_type: str = Field(..., example="CHEQUE_BOOK_ISSUE", description="CHEQUE_BOOK_ISSUE, CARD_BLOCK, ADDRESS_UPDATE, DISPUTE")
    details: Dict[str, Any] = Field(..., example={"account_number": "101000000012", "leaves": 50})
    submitted_at: str = Field(..., example="2026-09-07T04:20:00Z")
    status: str = Field(default="PENDING", example="PENDING", description="PENDING, APPROVED, REJECTED, COMPLETED")
    assigned_to: Optional[str] = Field(default="rajesh.amin", example="rajesh.amin")


class ServiceRequestActionRequest(BaseModel):
    action: str = Field(..., example="APPROVE", description="APPROVE, REJECT, DISPATCH")
    remarks: str = Field(..., example="Cheque book dispatched via BlueDart courier")
    tracking_number: Optional[str] = Field(default="BD99281023", example="BD99281023")


# ==========================================================
# 5. Reports & Audit Trail (US-23)
# ==========================================================

class AuditLogRecord(BaseModel):
    log_id: str = Field(..., example="AUDIT-20260907-0091")
    timestamp: str = Field(..., example="2026-09-07T05:45:12Z")
    admin_user: str = Field(..., example="rajesh.amin")
    action_type: str = Field(..., example="CIF_STATUS_UPDATE", description="CIF_STATUS_UPDATE, AUTH_RULE_MODIFIED, TXN_OVERRIDE, THEME_UPDATE")
    target_resource_id: str = Field(..., example="CIF100001")
    ip_address: str = Field(default="10.20.4.115", example="10.20.4.115")
    old_value: Optional[Dict[str, Any]] = None
    new_value: Optional[Dict[str, Any]] = None
    status: str = Field(default="SUCCESS", example="SUCCESS")


class ReportExportRequest(BaseModel):
    report_type: str = Field(..., example="TRANSACTIONS", description="TRANSACTIONS, AUDIT_TRAIL, CUSTOMER_SUMMARY, SERVICE_REQUESTS")
    from_date: str = Field(..., example="2026-08-01")
    to_date: str = Field(..., example="2026-09-07")
    format: str = Field(default="CSV", example="CSV", description="CSV, EXCEL, PDF")
    filter_params: Optional[Dict[str, Any]] = None


class ReportExportResponse(BaseModel):
    export_id: str = Field(..., example="EXP-20260907-001")
    report_name: str = Field(..., example="BharatBank_Transaction_Report_Aug_Sep_2026.csv")
    download_url: str = Field(..., example="https://reports.bharatbank.com/exports/EXP-20260907-001.csv")
    generated_at: str = Field(..., example="2026-09-07T06:30:00Z")
    record_count: int = Field(..., example=1250)
    file_size_kb: float = Field(..., example=480.5)


class AdminThemeUpdateRequest(BaseModel):
    theme_id: str = Field(default="bharat_bank_modern_v1", example="bharat_bank_modern_v1")
    is_dark_mode_configured: bool = Field(default=True, example=True)
    light_colors: ColorPalette
    dark_colors: ColorPalette
    typography: TypographyConfig
    logo_url: str = Field(..., example="https://assets.bharatbank.com/branding/logo-standard.png")
    light_logo_url: str = Field(..., example="https://assets.bharatbank.com/branding/logo-light.png")
    dark_logo_url: str = Field(..., example="https://assets.bharatbank.com/branding/logo-dark.png")
    favicon_url: str = Field(..., example="https://assets.bharatbank.com/branding/favicon.ico")
    app_name: str = Field(..., example="Bharat Bank")
    brand_tagline: str = Field(..., example="Empowering Every Indian with Smart Banking")

# ==========================================================
# 6. CBS Account Operations Schemas (Freeze, Lien, Limits)
# ==========================================================

class AdminAccountItem(BaseModel):
    account_number: str = Field(..., example="101000000012")
    cif: str = Field(..., example="CIF100001")
    customer_name: str = Field(..., example="Arjun Mehta")
    account_type: str = Field(..., example="SAVINGS", description="SAVINGS, CURRENT, SALARY, CORPORATE")
    product_code: str = Field(default="SB001", example="SB001")
    available_balance: float = Field(..., example=482450.00)
    ledger_balance: float = Field(..., example=482450.00)
    lien_amount: float = Field(default=0.00, example=0.00)
    status: str = Field(default="ACTIVE", example="ACTIVE", description="ACTIVE, FROZEN_DEBIT, FROZEN_CREDIT, FROZEN_TOTAL, DORMANT")
    freeze_reason: Optional[str] = None
    branch_code: str = Field(default="001", example="001")
    branch_name: str = Field(default="Nariman Point Branch", example="Nariman Point Branch")
    ifsc: str = Field(default="APEX0001048", example="APEX0001048")
    currency: str = Field(default="INR", example="INR")
    open_date: str = Field(default="2024-01-15", example="2024-01-15")


class AccountFreezeActionRequest(BaseModel):
    freeze_type: str = Field(default="DEBIT", example="DEBIT", description="DEBIT, CREDIT, FULL, LIEN")
    reason_code: str = Field(default="KYC_PENDING", example="KYC_PENDING", description="KYC_PENDING, COURT_ORDER, SUSPECTED_FRAUD, CUSTOMER_REQUEST")
    remarks: Optional[str] = Field(default="Compliance review hold", example="Compliance review hold")


class AccountUnfreezeActionRequest(BaseModel):
    reason_code: str = Field(default="KYC_VERIFIED", example="KYC_VERIFIED")
    remarks: Optional[str] = Field(default="KYC verification completed by compliance", example="KYC verification completed")


class AccountLienItem(BaseModel):
    lien_id: str = Field(..., example="LIEN-001")
    account_number: str = Field(..., example="101000000012")
    lien_amount: float = Field(..., example=25000.00)
    reason: str = Field(..., example="COLLATERAL_HOLD", description="COLLATERAL_HOLD, COURT_ATTACHMENT, CLEARING_HOLD")
    marked_by: str = Field(default="rajesh.amin", example="rajesh.amin")
    marked_at: str = Field(default="2026-09-01T10:00:00Z")
    status: str = Field(default="ACTIVE", example="ACTIVE")


class MarkLienRequest(BaseModel):
    lien_amount: float = Field(..., example=25000.00)
    reason: str = Field(default="COLLATERAL_HOLD", example="COLLATERAL_HOLD")
    reference_number: Optional[str] = Field(default="LN101000001", example="LN101000001")
    remarks: Optional[str] = Field(default="Lien against overdraft facility", example="Lien against overdraft facility")


class BalanceAdjustmentRequest(BaseModel):
    adjustment_type: str = Field(..., example="CREDIT", description="CREDIT or DEBIT")
    amount: float = Field(..., example=1500.00)
    gl_code: str = Field(default="GL-SUSPENSE-001", example="GL-SUSPENSE-001")
    reason: str = Field(..., example="Compensation for disputed chargeback resolution")
    checker_user_id: Optional[str] = Field(default="priya.sharma", example="priya.sharma")


# ==========================================================
# 7. Loan Underwriting & RPM Origination Schemas
# ==========================================================

class RPMApplicationSummary(BaseModel):
    application_no: str = Field(..., example="APP202609040001")
    process_ref_no: str = Field(..., example="PRC99881122")
    cif: str = Field(default="CIF100001", example="CIF100001")
    customer_name: str = Field(..., example="Arjun Mehta")
    mobile_number: str = Field(..., example="9876543210")
    product_type: str = Field(..., example="LOAN")
    product_sub_type: str = Field(..., example="HOME_LOAN", description="HOME_LOAN, PERSONAL_LOAN, AUTO_LOAN, MSME_LOAN")
    business_product_name: str = Field(..., example="Prime Home Loan")
    requested_amount: float = Field(..., example=3000000.00)
    tenure_months: int = Field(..., example=180)
    interest_rate: float = Field(default=8.50, example=8.50)
    channel: str = Field(default="OBDX", example="OBDX")
    status: str = Field(default="UNDER_REVIEW", example="UNDER_REVIEW", description="INITIATED, UNDER_REVIEW, DOCUMENTS_PENDING, SANCTIONED, DISBURSED, REJECTED")
    applied_date: str = Field(default="2026-09-04", example="2026-09-04")
    risk_score: int = Field(default=780, example=780)


class LoanDocumentItem(BaseModel):
    document_id: str = Field(..., example="DOC001")
    document_name: str = Field(..., example="Identity Proof (Aadhaar / Passport)")
    document_type: str = Field(..., example="KYC")
    mandatory: bool = Field(default=True, example=True)
    status: str = Field(default="VERIFIED", example="VERIFIED", description="PENDING, VERIFIED, REJECTED")
    file_url: Optional[str] = Field(default="https://docs.bharatbank.com/rpm/doc001.pdf")
    verified_by: Optional[str] = Field(default="priya.sharma")


class LoanUnderwritingDecisionRequest(BaseModel):
    decision: str = Field(..., example="APPROVE", description="APPROVE, REJECT, COUNTER_OFFER")
    sanctioned_amount: Optional[float] = Field(default=3000000.00, example=3000000.00)
    sanctioned_interest_rate: Optional[float] = Field(default=8.50, example=8.50)
    sanctioned_tenure_months: Optional[int] = Field(default=180, example=180)
    remarks: str = Field(..., example="Credit score 780, debt-to-income 32%. Approved.")


class LoanDisbursementRequest(BaseModel):
    disbursement_account_number: str = Field(..., example="101000000012")
    amount: float = Field(..., example=3000000.00)
    disbursement_mode: str = Field(default="INTERNAL_TRANSFER", example="INTERNAL_TRANSFER")
    notes: Optional[str] = Field(default="Tranche 1 disbursement for property acquisition", example="Tranche 1 disbursement")


# ==========================================================
# 8. Cheque CTS Clearing Operations Schemas
# ==========================================================

class InwardChequeClearingItem(BaseModel):
    cheque_id: str = Field(..., example="CTS-CLR-0091")
    cheque_number: str = Field(..., example="100001")
    drawer_account_number: str = Field(..., example="101000000012")
    drawer_name: str = Field(..., example="Arjun Mehta")
    presenting_bank_ifsc: str = Field(..., example="HDFC0000456")
    presenting_bank_name: str = Field(..., example="HDFC Bank")
    amount: float = Field(..., example=5000.00)
    clearing_cycle: str = Field(default="CTS GRID 1", example="CTS GRID 1")
    clearing_date: str = Field(default="2026-09-07", example="2026-09-07")
    status: str = Field(default="PENDING", example="PENDING", description="PENDING, CLEARED, RETURNED")
    cheque_image_front: str = Field(default="https://cts.bharatbank.com/cheques/100001_front.jpg")
    cheque_image_back: str = Field(default="https://cts.bharatbank.com/cheques/100001_back.jpg")


class ChequeClearingActionRequest(BaseModel):
    action: str = Field(..., example="CLEAR", description="CLEAR or RETURN")
    return_reason_code: Optional[str] = Field(default=None, example="FUNDS_INSUFFICIENT", description="FUNDS_INSUFFICIENT, SIGNATURE_MISMATCHES, CHEQUE_STOPPED")
    remarks: Optional[str] = Field(default="Authorized by clearing officer", example="Authorized by clearing officer")


class ChequeBookInventoryItem(BaseModel):
    branch_code: str = Field(..., example="001")
    branch_name: str = Field(..., example="Nariman Point Branch")
    stock_25_leaves: int = Field(..., example=120)
    stock_50_leaves: int = Field(..., example=85)
    stock_100_leaves: int = Field(..., example=40)
    last_replenished_on: str = Field(default="2026-08-20", example="2026-08-20")


# ==========================================================
# 9. Lockers & Branch Operations Schemas (CBS v3)
# ==========================================================

class BranchDetailItem(BaseModel):
    branch_code: str = Field(..., example="001")
    branch_name: str = Field(..., example="Nariman Point Branch")
    ifsc: str = Field(default="APEX0001048", example="APEX0001048")
    micr: str = Field(default="400002001", example="400002001")
    city: str = Field(default="Mumbai", example="Mumbai")
    branch_manager: str = Field(default="Deepak Verma", example="Deepak Verma")
    cash_in_vault: float = Field(default=12500000.00, example=12500000.00)
    lockers_total: int = Field(default=250, example=250)
    lockers_occupied: int = Field(default=215, example=215)
    is_active: bool = Field(default=True, example=True)


class LockerInventoryItem(BaseModel):
    locker_id: str = Field(..., example="LCK-001-A12")
    branch_code: str = Field(..., example="001")
    locker_type: str = Field(..., example="SMALL", description="SMALL, MEDIUM, LARGE, EXTRA_LARGE")
    annual_rent: float = Field(..., example=1500.00)
    status: str = Field(default="AVAILABLE", example="AVAILABLE", description="AVAILABLE, OCCUPIED, BLOCKED")
    allotted_to_cif: Optional[str] = None
    allotment_date: Optional[str] = None


class LockerAllotmentRequest(BaseModel):
    locker_id: str = Field(..., example="LCK-001-A12")
    cif: str = Field(..., example="CIF100001")
    debit_account_number: str = Field(..., example="101000000012")
    operating_instructions: str = Field(default="SINGLE", example="SINGLE", description="SINGLE, EITHER_OR_SURVIVOR, JOINTLY")


# ==========================================================
# 10. Reconciliation & Settlement Schemas
# ==========================================================

class SettlementBatchItem(BaseModel):
    batch_id: str = Field(..., example="SETTLE-20260907-IMPS-01")
    payment_rail: str = Field(..., example="IMPS", description="IMPS, NEFT, RTGS, BBPS, ATM")
    settlement_cycle: str = Field(..., example="CYCLE_01 (00:00 - 06:00)")
    total_txns: int = Field(..., example=1420)
    total_volume: float = Field(..., example=18950000.00)
    matched_txns: int = Field(..., example=1418)
    unreconciled_txns: int = Field(..., example=2)
    status: str = Field(default="RECONCILED", example="RECONCILED", description="PENDING, IN_PROGRESS, RECONCILED, DISCREPANCY")
    reconciled_at: str = Field(default="2026-09-07T06:30:00Z")


class ReconciliationExceptionItem(BaseModel):
    exception_id: str = Field(..., example="EXC-9912")
    batch_id: str = Field(..., example="SETTLE-20260907-IMPS-01")
    txn_ref: str = Field(..., example="TXN-20260907-88912")
    utr: str = Field(..., example="UTR-IMPS-20260907-99120")
    amount: float = Field(..., example=5000.00)
    issue_type: str = Field(..., example="SWITCH_TIMEOUT", description="SWITCH_TIMEOUT, NPCI_NOT_FOUND, CBS_FAIL_NPCI_SUCCESS")
    resolution_status: str = Field(default="OPEN", example="OPEN", description="OPEN, RESOLVED, ESCALATED")

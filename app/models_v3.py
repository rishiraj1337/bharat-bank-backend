from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# ==========================================================
# Common Envelopes & Header Models (Oracle CBS & FLEXCUBE)
# ==========================================================

class CBSHeaderV3(BaseModel):
    MessageId: str = Field(default="MSG20260904001", example="MSG20260904001", description="Unique message trace identifier")
    CorrelationId: str = Field(default="CORR123456", example="CORR123456", description="End-to-end correlation identifier")
    ChannelId: str = Field(default="MOBILE", example="MOBILE", description="Originating channel (MOBILE, OBDX, BRANCH, ATM)")
    UserId: str = Field(default="APIUSER", example="APIUSER", description="API User executing the request")
    BranchCode: str = Field(default="001", example="001", description="Branch identifier")
    RequestTimestamp: str = Field(default="2026-09-04T10:00:00", example="2026-09-04T10:00:00", description="ISO 8601 Timestamp")


class StatusResponseV3(BaseModel):
    Status: str = Field(default="SUCCESS", example="SUCCESS", description="Operation status")
    ReferenceNumber: str = Field(default="REF123456", example="REF123456", description="Unique transaction/audit reference number")
    Message: Optional[str] = Field(default="Operation completed successfully", example="Operation completed successfully", description="Status description message")


class ErrorResponseV3(BaseModel):
    ErrorCode: str = Field(default="BCB-001", example="BCB-001", description="FLEXCUBE standard error code")
    ErrorDescription: str = Field(default="Customer Not Found", example="Customer Not Found", description="Detailed error description")
    Severity: str = Field(default="ERROR", example="ERROR", description="Severity level: ERROR, WARNING, INFO")


class PagingDtoV3(BaseModel):
    totalResults: int = Field(default=1, example=1, description="Total number of records available")
    offset: int = Field(default=0, example=0, description="Pagination offset")
    limit: int = Field(default=10, example=10, description="Maximum number of items per page")


class ResponseCodeV3(BaseModel):
    Code: str = Field(default="00", example="00")
    Desc: str = Field(default="Success", example="Success")
    Type: Optional[str] = Field(default="I", example="I")
    Language: Optional[str] = Field(default="ENG", example="ENG")
    arg: Optional[str] = None


class ResponseDtoV3(BaseModel):
    id: str = Field(default="MSG2026090401", example="MSG2026090401")
    status: str = Field(default="SUCCESS", example="SUCCESS")
    codes: Optional[List[ResponseCodeV3]] = Field(default_factory=list)
    requestId: str = Field(default="REQ998811", example="REQ998811")


# ==========================================================
# 1. Customer & Account Information (Enriched 360)
# ==========================================================

class JointHolderV3(BaseModel):
    CustomerId: str = Field(..., example="CIF100002")
    Name: str = Field(..., example="Jane Doe")
    Relationship: Optional[str] = Field(default="JOINT_HOLDER", example="JOINT_HOLDER")


class NomineeV3(BaseModel):
    Name: str = Field(..., example="Nominee One")
    Relation: Optional[str] = Field(default="SPOUSE", example="SPOUSE")
    SharePercentage: Optional[int] = Field(default=100, example=100)


class DebitCardSummaryV3(BaseModel):
    CardNumber: str = Field(..., example="XXXXXX1234")
    CardType: str = Field(default="DEBIT", example="DEBIT")
    Status: str = Field(default="ACTIVE", example="ACTIVE")
    ExpiryDate: str = Field(default="2029-12-31", example="2029-12-31")


class AccountDetailItemV3(BaseModel):
    AccountNumber: str = Field(..., example="101000000001")
    AccountType: str = Field(..., example="SAVINGS", description="SAVINGS, CURRENT, SALARY")
    ProductCode: str = Field(default="SB001", example="SB001")
    ProductName: Optional[str] = Field(default="Premium Savings Account", example="Premium Savings Account")
    Currency: str = Field(default="INR", example="INR")
    BranchCode: str = Field(default="001", example="001")
    BranchName: Optional[str] = Field(default="Main Metro Branch", example="Main Metro Branch")
    IFSC: Optional[str] = Field(default="OBDX0000001", example="OBDX0000001")
    MICR: Optional[str] = Field(default="110002001", example="110002001")
    LedgerBalance: float = Field(..., example=120000.00)
    AvailableBalance: float = Field(..., example=118000.00)
    LienAmount: Optional[float] = Field(default=2000.00, example=2000.00)
    UnclearedBalance: Optional[float] = Field(default=0.00, example=0.00)
    InterestRate: Optional[float] = Field(default=4.5, example=4.5)
    Status: str = Field(default="ACTIVE", example="ACTIVE", description="ACTIVE, INACTIVE, DORMANT, FROZEN")
    OpenDate: Optional[str] = Field(default="2024-01-15", example="2024-01-15")
    NomineeRegistered: Optional[bool] = Field(default=True, example=True)
    ChequeBookFacility: Optional[bool] = Field(default=True, example=True)
    DebitCardActive: Optional[bool] = Field(default=True, example=True)
    JointHolders: Optional[Dict[str, List[JointHolderV3]]] = None
    Nominees: Optional[Dict[str, List[NomineeV3]]] = None
    Cards: Optional[Dict[str, List[DebitCardSummaryV3]]] = None


class CustomerProfileV3(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    CustomerName: str = Field(..., example="John Doe")
    CustomerType: str = Field(default="INDIVIDUAL", example="INDIVIDUAL", description="INDIVIDUAL, CORPORATE, NRI")
    MobileNumber: str = Field(default="9876543210", example="9876543210")
    EmailId: str = Field(default="john@email.com", example="john@email.com")
    KycStatus: str = Field(default="COMPLETED", example="COMPLETED", description="COMPLETED, PENDING, EXPIRED")


class CustomerAccountInquiryRequestV3(BaseModel):
    CustomerId: str = Field(..., example="CIF100001", description="Customer unique CIF ID")


class CustomerAccountInquiryResponseV3(BaseModel):
    Customer: CustomerProfileV3
    Accounts: Dict[str, List[AccountDetailItemV3]]


class CustomerAccountBasicInquiryRequestV3(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")


class BasicAccountItemV3(BaseModel):
    AccountNumber: str = Field(..., example="101000000001")
    AccountType: str = Field(..., example="SAVINGS")
    AvailableBalance: float = Field(..., example=118000.00)
    LedgerBalance: Optional[float] = Field(default=120000.00, example=120000.00)
    Currency: Optional[str] = Field(default="INR", example="INR")


class CustomerAccountBasicInquiryResponseV3(BaseModel):
    Customer: CustomerProfileV3
    Accounts: Dict[str, List[BasicAccountItemV3]]


class AccountDetailsInquiryRequestV3(BaseModel):
    AccountId: str = Field(..., example="101000000001", description="12-digit CBS Account Number")


class AccountDetailsInquiryResponseV3(BaseModel):
    Account: AccountDetailItemV3
    Cards: Optional[Dict[str, List[DebitCardSummaryV3]]] = None
    RelatedParties: Optional[Dict[str, List[JointHolderV3]]] = None
    Nominees: Optional[Dict[str, List[NomineeV3]]] = None


# ==========================================================
# 2. Account Actions & Statements
# ==========================================================

class AccountOpeningBalanceRequestV3(BaseModel):
    AccountId: str = Field(..., example="101000000001")
    AsOnDate: str = Field(default="2026-09-01", example="2026-09-01", description="Date in YYYY-MM-DD format")


class AccountOpeningBalanceResponseV3(BaseModel):
    AccountId: str = Field(..., example="101000000001")
    OpeningBalance: float = Field(..., example=100000.00)
    Currency: str = Field(default="INR", example="INR")
    AsOnDate: str = Field(default="2026-09-01", example="2026-09-01")


class AccountFreezeRequestV3(BaseModel):
    AccountId: str = Field(..., example="101000000001")
    FreezeType: str = Field(default="DEBIT", example="DEBIT", description="DEBIT, CREDIT, FULL, LIEN")
    ReasonCode: str = Field(default="KYC_PENDING", example="KYC_PENDING", description="Reason code from CBS catalogue")


class AccountUnfreezeRequestV3(BaseModel):
    AccountId: str = Field(..., example="101000000001")
    ReasonCode: Optional[str] = Field(default="KYC_VERIFIED", example="KYC_VERIFIED")


class TransactionRecordV3(BaseModel):
    TransactionId: str = Field(..., example="TXN202609040001")
    TransactionDate: str = Field(..., example="2026-09-02")
    ValueDate: str = Field(..., example="2026-09-02")
    Type: str = Field(..., example="DEBIT", description="DEBIT or CREDIT")
    Amount: float = Field(..., example=2500.00)
    Currency: str = Field(default="INR", example="INR")
    BalanceAfter: float = Field(..., example=118000.00)
    Narration: str = Field(..., example="UPI/Swiggy/Food Order/REF8829")
    ReferenceNo: str = Field(..., example="UPI-88291002")
    Channel: str = Field(default="MOBILE", example="MOBILE")


class AccountStatementRequestV3(BaseModel):
    AccountId: str = Field(..., example="101000000001")
    FromDate: Optional[str] = Field(default="2026-08-01", example="2026-08-01")
    ToDate: Optional[str] = Field(default="2026-09-04", example="2026-09-04")
    Offset: Optional[int] = Field(default=0, example=0)
    Limit: Optional[int] = Field(default=10, example=10)


class AccountStatementResponseV3(BaseModel):
    AccountId: str = Field(..., example="101000000001")
    FromDate: str = Field(..., example="2026-08-01")
    ToDate: str = Field(..., example="2026-09-04")
    OpeningBalance: float = Field(..., example=135000.00)
    ClosingBalance: float = Field(..., example=118000.00)
    TotalDebits: float = Field(..., example=22000.00)
    TotalCredits: float = Field(..., example=5000.00)
    Transactions: Dict[str, List[TransactionRecordV3]]
    Paging: PagingDtoV3


# ==========================================================
# 3. Cards Management
# ==========================================================

class CardStatusUpdateRequestV3(BaseModel):
    AccountId: str = Field(..., example="101000000001")
    CardNumber: str = Field(..., example="1234567890123456")
    NewCardStatus: str = Field(..., example="BLOCKED", description="ACTIVE, BLOCKED, HOTLISTED, CLOSED")
    Reason: Optional[str] = Field(default="CUSTOMER_REQUEST", example="CUSTOMER_REQUEST")


class CardInquiryRequestV3(BaseModel):
    AccountId: str = Field(..., example="101000000001")


class CardInquiryResponseV3(BaseModel):
    AccountId: str = Field(..., example="101000000001")
    Cards: Dict[str, List[DebitCardSummaryV3]]


# ==========================================================
# 4. Cheque Operations
# ==========================================================

class ChequeIssuedSummaryRequestV3(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    FromDate: Optional[str] = Field(default="2026-01-01", example="2026-01-01")
    ToDate: Optional[str] = Field(default="2026-12-31", example="2026-12-31")


class ChequeIssuedSummaryResponseV3(BaseModel):
    CustomerId: str = Field(default="CIF100001", example="CIF100001")
    TotalCheques: int = Field(..., example=15)
    TotalAmount: float = Field(..., example=350000.00)


class ChequeIssuedDetailItemV3(BaseModel):
    ChequeNumber: str = Field(..., example="100001")
    IssueDate: str = Field(..., example="2026-01-10")
    Amount: float = Field(..., example=5000.00)
    Status: str = Field(..., example="ISSUED", description="ISSUED, CLEARED, PASSED, STOPPED")
    Beneficiary: str = Field(..., example="ABC TRADERS")


class ChequeIssuedDetailRequestV3(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    FromDate: Optional[str] = Field(default="2026-01-01", example="2026-01-01")
    ToDate: Optional[str] = Field(default="2026-12-31", example="2026-12-31")


class ChequeIssuedDetailResponseV3(BaseModel):
    Cheques: Dict[str, List[ChequeIssuedDetailItemV3]]


class ChequeDepositedSummaryRequestV3(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    FromDate: Optional[str] = Field(default="2026-01-01", example="2026-01-01")
    ToDate: Optional[str] = Field(default="2026-12-31", example="2026-12-31")


class ChequeDepositedSummaryResponseV3(BaseModel):
    CustomerId: str = Field(default="CIF100001", example="CIF100001")
    TotalCheques: int = Field(..., example=8)
    TotalAmount: float = Field(..., example=140000.00)


class ChequeDepositedDetailItemV3(BaseModel):
    ChequeNumber: str = Field(..., example="550001")
    DepositDate: str = Field(..., example="2026-08-01")
    Amount: float = Field(..., example=25000.00)
    Status: str = Field(..., example="CLEARED", description="CLEARED, IN_PROCESS, RETURNED")


class ChequeDepositedDetailRequestV3(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    FromDate: Optional[str] = Field(default="2026-01-01", example="2026-01-01")
    ToDate: Optional[str] = Field(default="2026-12-31", example="2026-12-31")


class ChequeDepositedDetailResponseV3(BaseModel):
    Cheques: Dict[str, List[ChequeDepositedDetailItemV3]]


class ChequeStatusRequestV3(BaseModel):
    AccountId: str = Field(..., example="101000000001")
    ChequeNumber: str = Field(..., example="100001")


class ChequeStatusResponseV3(BaseModel):
    ChequeNumber: str = Field(..., example="100001")
    Status: str = Field(..., example="PASSED", description="PASSED, STOPPED, CLEARED, RETURNED, ISSUED")
    Amount: float = Field(..., example=5000.00)
    TransactionDate: str = Field(..., example="2026-08-30")


class ChequeLeafStatusItemV3(BaseModel):
    ChequeNumber: str = Field(..., example="110001")
    Status: str = Field(..., example="USED", description="AVAILABLE, USED, STOPPED, CANCELLED")


class ChequeLeavesStatusRequestV3(BaseModel):
    AccountId: str = Field(..., example="101000000001")


class ChequeLeavesStatusResponseV3(BaseModel):
    Cheques: Dict[str, List[ChequeLeafStatusItemV3]]


class ChequeStopPaymentRequestV3(BaseModel):
    AccountId: str = Field(..., example="101000000001")
    ChequeNumber: str = Field(..., example="110003")
    Reason: str = Field(default="LOST_OR_STOLEN", example="LOST_OR_STOLEN")


# ==========================================================
# 5. Certificates & Compliance
# ==========================================================

class InterestCertificateRequestV3(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    FinancialYear: Optional[str] = Field(default="2026", example="2026")


class InterestCertificateResponseV3(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    FinancialYear: str = Field(..., example="2026")
    InterestEarned: float = Field(..., example=15432.56)
    Currency: str = Field(default="INR", example="INR")


class TDSCertificateRequestV3(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    FinancialYear: Optional[str] = Field(default="2026", example="2026")


class TDSCertificateResponseV3(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    FinancialYear: str = Field(..., example="2026")
    TDSDeducted: float = Field(..., example=1543.26)
    Currency: str = Field(default="INR", example="INR")


# ==========================================================
# 6. Lockers & Mobile Validation
# ==========================================================

class LockerItemV3(BaseModel):
    LockerType: str = Field(..., example="SMALL", description="SMALL, MEDIUM, LARGE, EXTRA_LARGE")
    AvailableCount: int = Field(..., example=20)
    AnnualRent: float = Field(..., example=1500.00)


class LockerInquiryRequestV3(BaseModel):
    BranchCode: Optional[str] = Field(default="001", example="001")


class LockerInquiryResponseV3(BaseModel):
    BranchCode: str = Field(default="001", example="001")
    Lockers: Dict[str, List[LockerItemV3]]


class MobileValidationRequestV3(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    MobileNumber: str = Field(..., example="9876543210")


class MobileValidationResponseV3(BaseModel):
    Valid: bool = Field(..., example=True)
    Message: str = Field(..., example="Mobile Number Matched")


# ==========================================================
# 7. Loans Management & Amortization
# ==========================================================

class LoanItemV3(BaseModel):
    LoanAccountNumber: str = Field(..., example="LN1010000001")
    LoanType: str = Field(..., example="HOME_LOAN", description="HOME_LOAN, AUTO_LOAN, PERSONAL_LOAN")
    SanctionedAmount: float = Field(..., example=5000000.00)
    OutstandingPrincipal: float = Field(..., example=4250000.00)
    InterestRate: float = Field(..., example=8.5)
    TenureMonths: int = Field(..., example=240)
    RemainingTenureMonths: int = Field(..., example=195)
    EMIAmount: float = Field(..., example=43391.00)
    NextDueDate: str = Field(..., example="2026-09-10")
    Status: str = Field(default="ACTIVE", example="ACTIVE")


class LoanInquiryRequestV3(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")


class LoanInquiryResponseV3(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    Loans: Dict[str, List[LoanItemV3]]


class AmortizationScheduleItemV3(BaseModel):
    InstallmentNo: int = Field(..., example=1)
    DueDate: str = Field(..., example="2026-09-10")
    PrincipalComponent: float = Field(..., example=13308.00)
    InterestComponent: float = Field(..., example=30083.00)
    TotalInstallment: float = Field(..., example=43391.00)
    EndingBalance: float = Field(..., example=4236692.00)


class LoanScheduleRequestV3(BaseModel):
    LoanAccountNumber: str = Field(..., example="LN1010000001")


class LoanScheduleResponseV3(BaseModel):
    LoanAccountNumber: str = Field(..., example="LN1010000001")
    InterestRate: float = Field(..., example=8.5)
    Schedule: Dict[str, List[AmortizationScheduleItemV3]]


class LoanApplyRequestV3(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    LoanType: str = Field(default="HOME_LOAN", example="HOME_LOAN")
    RequestedAmount: float = Field(..., example=3000000.00)
    TenureMonths: int = Field(..., example=180)
    MonthlyIncome: float = Field(..., example=120000.00)
    BranchCode: Optional[str] = Field(default="001", example="001")


class LoanApplyResponseV3(BaseModel):
    ApplicationNumber: str = Field(..., example="LNAPP20260904001")
    Status: str = Field(default="IN_REVIEW", example="IN_REVIEW")
    EstimatedEMI: float = Field(..., example=29570.00)
    Message: str = Field(default="Loan application received successfully", example="Loan application received successfully")


# ==========================================================
# 8. Term Deposits (FD / RD & Pre-closure)
# ==========================================================

class TermDepositItemV3(BaseModel):
    DepositAccountNumber: str = Field(..., example="FD1010000001")
    DepositType: str = Field(..., example="FIXED_DEPOSIT", description="FIXED_DEPOSIT or RECURRING_DEPOSIT")
    PrincipalAmount: float = Field(..., example=200000.00)
    InterestRate: float = Field(..., example=7.25)
    MaturityAmount: float = Field(..., example=231800.00)
    DepositDate: str = Field(..., example="2025-09-04")
    MaturityDate: str = Field(..., example="2027-09-04")
    InterestPayout: str = Field(default="ON_MATURITY", example="ON_MATURITY")
    AutoRenewal: bool = Field(default=True, example=True)
    Status: str = Field(default="ACTIVE", example="ACTIVE")


class TermDepositInquiryRequestV3(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")


class TermDepositInquiryResponseV3(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    Deposits: Dict[str, List[TermDepositItemV3]]


class TermDepositOpenRequestV3(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    DebitAccountNumber: str = Field(..., example="101000000001")
    DepositType: str = Field(default="FIXED_DEPOSIT", example="FIXED_DEPOSIT")
    Amount: float = Field(..., example=100000.00)
    TenureMonths: int = Field(..., example=12)
    InterestPayout: Optional[str] = Field(default="ON_MATURITY", example="ON_MATURITY")
    AutoRenewal: Optional[bool] = Field(default=True, example=True)


class TermDepositOpenResponseV3(BaseModel):
    DepositAccountNumber: str = Field(..., example="FD1010000099")
    PrincipalAmount: float = Field(..., example=100000.00)
    InterestRate: float = Field(..., example=7.1)
    MaturityAmount: float = Field(..., example=107300.00)
    MaturityDate: str = Field(..., example="2027-09-04")
    Status: str = Field(default="ACTIVE", example="ACTIVE")
    Message: str = Field(default="Term Deposit opened successfully", example="Term Deposit opened successfully")


class TDTrialClosureRequestV3(BaseModel):
    TDAccountId: str = Field(..., example="TD100001")


class TDTrialClosureResponseV3(BaseModel):
    TDAccountId: str = Field(..., example="TD100001")
    ClosureValue: float = Field(..., example=105000.00)
    PenaltyAmount: float = Field(..., example=500.00)
    NetPayable: float = Field(..., example=104500.00)


# ==========================================================
# 9. Payments, Upcoming Inflows & Transfers
# ==========================================================

class UpcomingPaymentItemV3(BaseModel):
    PaymentType: str = Field(..., example="EMI", description="EMI, BILL_PAYMENT, SI")
    DueDate: str = Field(..., example="2026-09-10")
    Amount: float = Field(..., example=12000.00)


class UpcomingPaymentsRequestV3(BaseModel):
    CustomerId: Optional[str] = Field(default="CIF100001", example="CIF100001")


class UpcomingPaymentsResponseV3(BaseModel):
    CustomerId: str = Field(default="CIF100001", example="CIF100001")
    Payments: Dict[str, List[UpcomingPaymentItemV3]]


class UpcomingIncomeItemV3(BaseModel):
    IncomeType: str = Field(..., example="FD_INTEREST", description="FD_INTEREST, SALARY, DIVIDEND")
    CreditDate: str = Field(..., example="2026-09-15")
    Amount: float = Field(..., example=8500.00)


class UpcomingIncomeRequestV3(BaseModel):
    CustomerId: Optional[str] = Field(default="CIF100001", example="CIF100001")


class UpcomingIncomeResponseV3(BaseModel):
    CustomerId: str = Field(default="CIF100001", example="CIF100001")
    Incomes: Dict[str, List[UpcomingIncomeItemV3]]


class FundTransferRequestV3(BaseModel):
    DebtorAccount: str = Field(..., example="101000000001")
    CreditorAccount: str = Field(..., example="202000000002")
    BeneficiaryName: str = Field(..., example="Jane Doe")
    IFSC: Optional[str] = Field(default="OBDX0000001", example="OBDX0000001")
    Amount: float = Field(..., example=5000.00)
    Currency: Optional[str] = Field(default="INR", example="INR")
    PaymentMode: str = Field(default="IMPS", example="IMPS", description="INTERNAL, IMPS, NEFT, RTGS")
    Remarks: Optional[str] = Field(default="Monthly Rent", example="Monthly Rent")


class FundTransferResponseV3(BaseModel):
    TransactionReference: str = Field(..., example="FT20260904123456")
    Status: str = Field(default="SUCCESS", example="SUCCESS")
    DebtorAccount: str = Field(..., example="101000000001")
    Amount: float = Field(..., example=5000.00)
    Currency: str = Field(default="INR", example="INR")
    Timestamp: str = Field(..., example="2026-09-04T15:30:00")
    UTR: str = Field(..., example="UTR8839201928")
    Message: str = Field(default="Funds transferred successfully", example="Funds transferred successfully")


# ==========================================================
# 10. Oracle OBDX / RPM Origination & Products
# ==========================================================

class BusProdAggregateInquiryRequestV3(BaseModel):
    productType: Optional[str] = Field(default="LOAN", example="LOAN")
    channel: Optional[str] = Field(default="OBDX", example="OBDX")
    businessProductCode: Optional[str] = Field(default=None, example="HL001")


class ProcessInitiateRequestV3(BaseModel):
    channel: str = Field(default="OBDX", example="OBDX")
    productType: str = Field(default="LOAN", example="LOAN")
    productSubType: Optional[str] = Field(default="HOME_LOAN", example="HOME_LOAN")
    businessProductCode: Optional[str] = Field(default="HL001", example="HL001")
    custName: str = Field(default="John Doe", example="John Doe")
    custMobile: str = Field(default="9876543210", example="9876543210")
    custEmail: Optional[str] = Field(default="john.doe@email.com", example="john.doe@email.com")
    branchCode: Optional[str] = Field(default="001", example="001")


class ProcessInitiateResponseV3(BaseModel):
    messages: ResponseDtoV3
    applicationNumber: str = Field(..., example="APP202609040001")
    processRefNo: str = Field(..., example="PRC99881122")
    status: str = Field(default="INITIATED", example="INITIATED")


class ProcessSubmitRequestV3(BaseModel):
    channel: str = Field(default="OBDX", example="OBDX")
    action: str = Field(default="SUBMIT", example="SUBMIT", description="SAVE or SUBMIT")
    applicationNumber: str = Field(..., example="APP202609040001")
    remarks: Optional[str] = Field(default="Application submitted via web portal", example="Application submitted")
    domainData: Optional[Dict[str, Any]] = None


class ProcessSubmitResponseV3(BaseModel):
    messages: ResponseDtoV3
    applicationNumber: str = Field(..., example="APP202609040001")
    status: str = Field(default="SUBMITTED", example="SUBMITTED")


class ProcessGetDataRequestV3(BaseModel):
    applicationNumber: str = Field(..., example="APP202609040001")


class ProcessGetDocumentListRequestV3(BaseModel):
    applicationNumber: Optional[str] = Field(default=None, example="APP202609040001")
    businessProductCode: Optional[str] = Field(default="HL001", example="HL001")
    productType: Optional[str] = Field(default="LOAN", example="LOAN")


class ApplicationsListInquiryRequestV3(BaseModel):
    fromDate: Optional[str] = Field(default="2026-08-01", example="2026-08-01")
    toDate: Optional[str] = Field(default="2026-09-04", example="2026-09-04")
    applicationNo: Optional[str] = Field(default=None, example="APP202609040001")
    processRefNo: Optional[str] = Field(default=None, example="PRC99881122")
    productType: Optional[str] = Field(default=None, example="LOAN")
    custName: Optional[str] = Field(default=None, example="John Doe")
    custMobile: Optional[str] = Field(default=None, example="9876543210")
    channel: Optional[str] = Field(default="OBDX", example="OBDX")
    offset: Optional[int] = Field(default=0, example=0)
    limit: Optional[int] = Field(default=10, example=10)

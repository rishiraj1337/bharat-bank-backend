from typing import List, Optional
from pydantic import BaseModel, Field

# --- Common Models ---
class CBSHeader(BaseModel):
    MessageId: Optional[str] = Field(default="MSG20260904001", description="Unique message identifier")
    CorrelationId: Optional[str] = Field(default="CORR123456", description="Correlation identifier")
    ChannelId: Optional[str] = Field(default="MOBILE", description="Channel identifier (MOBILE, BRANCH, ATM)")
    UserId: Optional[str] = Field(default="APIUSER", description="Calling API User")
    BranchCode: Optional[str] = Field(default="001", description="Branch identifier")
    RequestTimestamp: Optional[str] = Field(default="2026-09-04T10:00:00", description="ISO timestamp")


class StatusResponse(BaseModel):
    Status: str = Field(default="SUCCESS", description="Operation status")
    ReferenceNumber: str = Field(default="REF123456", description="Unique transaction reference")
    Message: Optional[str] = Field(default="Operation completed successfully", description="Status message")


class ErrorResponse(BaseModel):
    ErrorCode: str = Field(default="BCB-001", description="CBS standard error code")
    ErrorDescription: str = Field(default="Customer Not Found", description="Human readable description")
    Severity: str = Field(default="ERROR", description="Severity level: ERROR or WARNING")


# --- 1. Customer Account Inquiry ---
class CustomerAccountInquiryRequest(BaseModel):
    CustomerId: str = Field(..., example="CIF100001", description="Customer ID")


class JointHolderModel(BaseModel):
    CustomerId: str = Field(..., example="CIF100002")
    Name: str = Field(..., example="Jane Doe")


class NomineeModel(BaseModel):
    Name: str = Field(..., example="Nominee One")
    Relation: Optional[str] = Field(default="SPOUSE", example="SPOUSE")
    SharePercentage: Optional[int] = Field(default=100, example=100)


class AccountInfoModel(BaseModel):
    AccountNumber: str = Field(..., example="101000000001")
    AccountType: str = Field(..., example="SAVINGS")
    Currency: str = Field(default="INR", example="INR")
    LedgerBalance: float = Field(..., example=120000.00)
    AvailableBalance: float = Field(..., example=118000.00)
    Status: str = Field(default="ACTIVE", example="ACTIVE")
    JointHolders: Optional[dict] = None
    Nominees: Optional[dict] = None


class CustomerProfileModel(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    CustomerName: str = Field(..., example="John Doe")
    CustomerType: Optional[str] = Field(default="INDIVIDUAL", example="INDIVIDUAL")
    MobileNumber: Optional[str] = Field(default="9876543210", example="9876543210")
    EmailId: Optional[str] = Field(default="john@email.com", example="john@email.com")
    KycStatus: Optional[str] = Field(default="COMPLETED", example="COMPLETED")


class CustomerAccountInquiryResponse(BaseModel):
    Customer: CustomerProfileModel
    Accounts: dict


# --- 2. Customer Account Basic Inquiry ---
class CustomerAccountBasicInquiryRequest(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")


class BasicCustomerModel(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    CustomerName: str = Field(..., example="John Doe")


class BasicAccountModel(BaseModel):
    AccountNumber: str = Field(..., example="101000000001")
    AccountType: str = Field(..., example="SAVINGS")
    AvailableBalance: float = Field(..., example=118000.00)


class CustomerAccountBasicInquiryResponse(BaseModel):
    Customer: BasicCustomerModel
    Accounts: dict


# --- 3. Account Details Inquiry ---
class AccountDetailsInquiryRequest(BaseModel):
    AccountId: str = Field(..., example="101000000001")


class AccountDetailsInquiryResponse(BaseModel):
    Account: dict
    Cards: Optional[dict] = None
    RelatedParties: Optional[dict] = None
    Nominees: Optional[dict] = None


# --- 4. Account Opening Balance ---
class AccountOpeningBalanceRequest(BaseModel):
    AccountId: str = Field(..., example="101000000001")
    AsOnDate: Optional[str] = Field(default="2026-09-01", example="2026-09-01")


class AccountOpeningBalanceResponse(BaseModel):
    AccountId: str = Field(..., example="101000000001")
    OpeningBalance: float = Field(..., example=100000.00)
    Currency: str = Field(default="INR", example="INR")


# --- 5. Account Freeze ---
class AccountFreezeRequest(BaseModel):
    AccountId: str = Field(..., example="101000000001")
    FreezeType: str = Field(default="DEBIT", example="DEBIT", description="DEBIT, CREDIT, FULL, LIEN")
    ReasonCode: Optional[str] = Field(default="KYC_PENDING", example="KYC_PENDING")


# --- 6. Account Unfreeze ---
class AccountUnfreezeRequest(BaseModel):
    AccountId: str = Field(..., example="101000000001")


# --- 7. Card Status Update ---
class CardStatusUpdateRequest(BaseModel):
    AccountId: str = Field(..., example="101000000001")
    CardNumber: str = Field(..., example="1234567890123456")
    NewCardStatus: str = Field(..., example="BLOCKED", description="ACTIVE, BLOCKED, HOTLISTED, CLOSED")


# --- 8. Cheque Issued Summary ---
class ChequeIssuedSummaryRequest(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    FromDate: Optional[str] = Field(default="2026-01-01", example="2026-01-01")
    ToDate: Optional[str] = Field(default="2026-12-31", example="2026-12-31")


class ChequeIssuedSummaryResponse(BaseModel):
    TotalCheques: int = Field(..., example=15)
    TotalAmount: float = Field(..., example=350000.00)


# --- 9. Cheque Issued Detail ---
class ChequeIssuedDetailRequest(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    FromDate: Optional[str] = Field(default="2026-01-01", example="2026-01-01")
    ToDate: Optional[str] = Field(default="2026-12-31", example="2026-12-31")


class ChequeIssuedDetailResponse(BaseModel):
    Cheques: dict


# --- 10. Cheque Deposited Summary ---
class ChequeDepositedSummaryRequest(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    FromDate: Optional[str] = Field(default="2026-01-01", example="2026-01-01")
    ToDate: Optional[str] = Field(default="2026-12-31", example="2026-12-31")


class ChequeDepositedSummaryResponse(BaseModel):
    TotalCheques: int = Field(..., example=8)
    TotalAmount: float = Field(..., example=140000.00)


# --- 11. Cheque Deposited Detail ---
class ChequeDepositedDetailRequest(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    FromDate: Optional[str] = Field(default="2026-01-01", example="2026-01-01")
    ToDate: Optional[str] = Field(default="2026-12-31", example="2026-12-31")


class ChequeDepositedDetailResponse(BaseModel):
    Cheques: dict


# --- 12. Passed and Stopped Cheque Inquiry ---
class ChequeStatusRequest(BaseModel):
    AccountId: str = Field(..., example="101000000001")
    ChequeNumber: str = Field(..., example="100001")


class ChequeStatusResponse(BaseModel):
    ChequeNumber: str = Field(..., example="100001")
    Status: str = Field(..., example="PASSED", description="PASSED, STOPPED, CLEARED, RETURNED")
    Amount: float = Field(..., example=5000.00)
    TransactionDate: str = Field(..., example="2026-08-30")


# --- 13. Interest Certificate ---
class InterestCertificateRequest(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    FinancialYear: Optional[str] = Field(default="2026", example="2026")


class InterestCertificateResponse(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    FinancialYear: str = Field(..., example="2026")
    InterestEarned: float = Field(..., example=15432.56)


# --- 14. TDS Certificate ---
class TDSCertificateRequest(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    FinancialYear: Optional[str] = Field(default="2026", example="2026")


class TDSCertificateResponse(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    FinancialYear: str = Field(..., example="2026")
    TDSDeducted: float = Field(..., example=1543.26)


# --- 15. Locker Inquiry ---
class LockerInquiryRequest(BaseModel):
    BranchCode: Optional[str] = Field(default="001", example="001")


class LockerInquiryResponse(BaseModel):
    Lockers: dict


# --- 16. Mobile Validation ---
class MobileValidationRequest(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    MobileNumber: str = Field(..., example="9876543210")


class MobileValidationResponse(BaseModel):
    Valid: bool = Field(..., example=True)
    Message: str = Field(..., example="Mobile Number Matched")


# --- 17. TD Trial Closure ---
class TDTrialClosureRequest(BaseModel):
    TDAccountId: str = Field(..., example="TD100001")


class TDTrialClosureResponse(BaseModel):
    TDAccountId: str = Field(..., example="TD100001")
    ClosureValue: float = Field(..., example=105000.00)
    PenaltyAmount: float = Field(..., example=500.00)
    NetPayable: float = Field(..., example=104500.00)


# --- 18. Upcoming Payments ---
class UpcomingPaymentsRequest(BaseModel):
    CustomerId: Optional[str] = Field(default="CIF100001", example="CIF100001")


class UpcomingPaymentsResponse(BaseModel):
    Payments: dict


# --- 19. Upcoming Income ---
class UpcomingIncomeRequest(BaseModel):
    CustomerId: Optional[str] = Field(default="CIF100001", example="CIF100001")


class UpcomingIncomeResponse(BaseModel):
    Incomes: dict


# --- 20. Cheque Leaves Status ---
class ChequeLeavesStatusRequest(BaseModel):
    AccountId: str = Field(..., example="101000000001")


class ChequeLeavesStatusResponse(BaseModel):
    Cheques: dict

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# --- Common / Wrapper Models ---
class ResponseCode(BaseModel):
    Code: str = Field(default="00", example="00")
    Desc: str = Field(default="Success", example="Success")
    Type: Optional[str] = Field(default="I", example="I")
    Language: Optional[str] = Field(default="ENG", example="ENG")
    arg: Optional[str] = None


class ResponseDto(BaseModel):
    id: Optional[str] = Field(default="RESP2026090401", example="RESP2026090401")
    status: str = Field(default="SUCCESS", example="SUCCESS")
    codes: Optional[List[ResponseCode]] = Field(default_factory=list)
    requestId: Optional[str] = Field(default="REQ998811", example="REQ998811")


class PagingDto(BaseModel):
    totalResults: int = Field(default=1, example=1)
    offset: Optional[int] = Field(default=0, example=0)
    limit: Optional[int] = Field(default=10, example=10)


# --- RPM: Business Products ---
class BusProdCcyConfigModel(BaseModel):
    currency: str = Field(default="INR", example="INR")
    minAmount: float = Field(default=10000.0, example=10000.0)
    maxAmount: float = Field(default=10000000.0, example=10000000.0)
    minTerm: int = Field(default=6, example=6)
    maxTerm: int = Field(default=360, example=360)
    minTermTenorBasis: Optional[str] = Field(default="M", example="M")
    maxTermTenorBasis: Optional[str] = Field(default="M", example="M")


class BusProdDecnboxModel(BaseModel):
    scorecardType: str = Field(default="INTERNAL", example="INTERNAL")
    minScore: float = Field(default=650.0, example=650.0)
    maxScore: float = Field(default=900.0, example=900.0)
    outcome: str = Field(default="ACCEPT", example="ACCEPT")
    serialNo: int = Field(default=1, example=1)


class BusProdPrefCompModel(BaseModel):
    autoRollover: Optional[str] = Field(default="Y", example="Y")
    chequebook: Optional[str] = Field(default="Y", example="Y")
    debitcard: Optional[str] = Field(default="Y", example="Y")
    directBanking: Optional[str] = Field(default="Y", example="Y")
    passbook: Optional[str] = Field(default="Y", example="Y")
    phoneBanking: Optional[str] = Field(default="Y", example="Y")
    BusProdCcyConfig: Optional[List[BusProdCcyConfigModel]] = None
    IntlScrCrdDecnboxDTO: Optional[List[BusProdDecnboxModel]] = None


class BusProdPrefServiceModel(BaseModel):
    businessProductCode: str = Field(..., example="HL001")
    productType: str = Field(..., example="LOAN")
    productSubType: Optional[str] = Field(default="HOME_LOAN", example="HOME_LOAN")
    channelAllowed: Optional[str] = Field(default="Y", example="Y")
    minAge: Optional[int] = Field(default=21, example=21)
    maxAge: Optional[int] = Field(default=65, example=65)
    BusProdPrefComp: Optional[BusProdPrefCompModel] = None


class BusProdDetailsServiceModel(BaseModel):
    businessProductCode: str = Field(..., example="HL001")
    businessProductName: str = Field(..., example="Prime Home Loan")
    businessProductDesc: Optional[str] = Field(default="Affordable home loan with low interest rates", example="Affordable home loan")
    productType: str = Field(..., example="LOAN")
    productSubType: Optional[str] = Field(default="HOME_LOAN", example="HOME_LOAN")
    startDate: Optional[str] = Field(default="2026-01-01", example="2026-01-01")
    expiryDate: Optional[str] = Field(default="2030-12-31", example="2030-12-31")


class BusProdAttrFeatureServiceModel(BaseModel):
    businessProductCode: str = Field(default="HL001", example="HL001")
    featureName: str = Field(default="Zero Prepayment Charges", example="Zero Prepayment Charges")
    featureDesc: Optional[str] = Field(default="No penalty on early repayment", example="No penalty on early repayment")


class BusProdAttrFeeChargesServiceModel(BaseModel):
    businessProductCode: str = Field(default="HL001", example="HL001")
    feeChargesName: str = Field(default="Processing Fee", example="Processing Fee")
    feeChargesDesc: Optional[str] = Field(default="0.5% of loan amount + GST", example="0.5% of loan amount")


class BusProdAttrServiceModel(BaseModel):
    businessProductCode: str = Field(..., example="HL001")
    productType: str = Field(..., example="LOAN")
    businessProductSummary: Optional[str] = Field(default="Best in class mortgage product", example="Best in class mortgage")
    BusProdAttrFeature: Optional[List[BusProdAttrFeatureServiceModel]] = None
    BusProdAttrFeeCharges: Optional[List[BusProdAttrFeeChargesServiceModel]] = None


class BusProdAggregateServiceModel(BaseModel):
    businessProductDetails: BusProdDetailsServiceModel
    businessProductPreferences: Optional[BusProdPrefServiceModel] = None
    businessProductAttr: Optional[BusProdAttrServiceModel] = None


class BusProdAggregateServiceModelCollection(BaseModel):
    data: List[BusProdAggregateServiceModel]
    paging: Optional[PagingDto] = None


# --- RPM: Process Driver ---
class BasicApplicationDetailsModel(BaseModel):
    channel: str = Field(default="OBDX", example="OBDX")
    productType: str = Field(default="LOAN", example="LOAN")
    productSubType: Optional[str] = Field(default="HOME_LOAN", example="HOME_LOAN")
    businessProductCode: Optional[str] = Field(default="HL001", example="HL001")
    custName: Optional[str] = Field(default="John Doe", example="John Doe")
    custMobile: Optional[str] = Field(default="9876543210", example="9876543210")
    custEmail: Optional[str] = Field(default="john.doe@email.com", example="john.doe@email.com")
    branchCode: Optional[str] = Field(default="001", example="001")


class ProcessInitiateResponse(BaseModel):
    messages: ResponseDto
    applicationNumber: str = Field(..., example="APP202609040001")
    processRefNo: str = Field(..., example="PRC99881122")
    status: str = Field(default="INITIATED", example="INITIATED")


class SubmitExtSystemRequest(BaseModel):
    channel: str = Field(default="OBDX", example="OBDX")
    action: str = Field(default="SUBMIT", example="SUBMIT", description="SAVE or SUBMIT")
    applicationNumber: str = Field(..., example="APP202609040001")
    remarks: Optional[str] = Field(default="Application submitted via web portal", example="Application submitted")
    domainData: Optional[Dict[str, Any]] = None


class SubmitExtSystemResponse(BaseModel):
    messages: ResponseDto
    applicationNumber: str = Field(..., example="APP202609040001")
    status: str = Field(default="SUBMITTED", example="SUBMITTED")


class DocumentModel(BaseModel):
    documentId: str = Field(default="DOC001", example="DOC001")
    documentName: str = Field(default="Identity Proof", example="Identity Proof")
    documentType: str = Field(default="KYC", example="KYC")
    mandatory: str = Field(default="Y", example="Y")
    status: str = Field(default="PENDING", example="PENDING")


class DocumentCollection(BaseModel):
    data: List[DocumentModel]


# --- RPM: Applications Inquiry ---
class ApplicationSummaryModel(BaseModel):
    applicationNo: str = Field(..., example="APP202609040001")
    processRefNo: str = Field(..., example="PRC99881122")
    applicationDate: str = Field(default="2026-09-04", example="2026-09-04")
    productType: str = Field(default="LOAN", example="LOAN")
    productSubType: Optional[str] = Field(default="HOME_LOAN", example="HOME_LOAN")
    businessProductName: Optional[str] = Field(default="Prime Home Loan", example="Prime Home Loan")
    custName: str = Field(default="John Doe", example="John Doe")
    custMobile: str = Field(default="9876543210", example="9876543210")
    custEmail: Optional[str] = Field(default="john.doe@email.com", example="john.doe@email.com")
    branchCode: str = Field(default="001", example="001")
    channel: str = Field(default="OBDX", example="OBDX")
    status: str = Field(default="IN_PROGRESS", example="IN_PROGRESS")


class ApplicationsListResponse(BaseModel):
    data: List[ApplicationSummaryModel]
    paging: PagingDto


# --- Extra Custom APIs: Account Info 360 ---
class AccountInfo360Response(BaseModel):
    AccountId: str = Field(..., example="101000000001")
    AccountNumber: str = Field(..., example="101000000001")
    CustomerId: str = Field(..., example="CIF100001")
    CustomerName: str = Field(..., example="John Doe")
    AccountType: str = Field(..., example="SAVINGS")
    ProductCode: str = Field(..., example="SB001")
    ProductName: str = Field(..., example="Premium Savings Account")
    Currency: str = Field(default="INR", example="INR")
    BranchCode: str = Field(default="001", example="001")
    BranchName: str = Field(default="Main Metro Branch", example="Main Metro Branch")
    IFSC: str = Field(default="OBDX0000001", example="OBDX0000001")
    MICR: str = Field(default="110002001", example="110002001")
    LedgerBalance: float = Field(..., example=120000.0)
    AvailableBalance: float = Field(..., example=118000.0)
    LienAmount: float = Field(default=2000.0, example=2000.0)
    UnclearedBalance: float = Field(default=0.0, example=0.0)
    InterestRate: float = Field(default=4.5, example=4.5)
    Status: str = Field(default="ACTIVE", example="ACTIVE")
    OpenDate: str = Field(default="2024-01-15", example="2024-01-15")
    NomineeRegistered: bool = Field(default=True, example=True)
    ChequeBookFacility: bool = Field(default=True, example=True)
    DebitCardActive: bool = Field(default=True, example=True)


# --- Extra Custom APIs: Account Statement ---
class TransactionRecord(BaseModel):
    TransactionId: str = Field(..., example="TXN202609040001")
    TransactionDate: str = Field(..., example="2026-09-02")
    ValueDate: str = Field(..., example="2026-09-02")
    Type: str = Field(..., example="DEBIT", description="DEBIT or CREDIT")
    Amount: float = Field(..., example=2500.0)
    Currency: str = Field(default="INR", example="INR")
    BalanceAfter: float = Field(..., example=118000.0)
    Narration: str = Field(..., example="UPI/Swiggy/Food Order/REF8829")
    ReferenceNo: str = Field(..., example="UPI-88291002")
    Channel: str = Field(default="MOBILE", example="MOBILE")


class AccountStatementResponse(BaseModel):
    AccountId: str = Field(..., example="101000000001")
    FromDate: str = Field(..., example="2026-08-01")
    ToDate: str = Field(..., example="2026-09-04")
    OpeningBalance: float = Field(..., example=135000.0)
    ClosingBalance: float = Field(..., example=118000.0)
    TotalDebits: float = Field(..., example=22000.0)
    TotalCredits: float = Field(..., example=5000.0)
    Transactions: List[TransactionRecord]
    Paging: PagingDto


# --- Extra Custom APIs: Loans ---
class LoanAccountModel(BaseModel):
    LoanAccountNumber: str = Field(..., example="LN1010000001")
    LoanType: str = Field(..., example="HOME_LOAN")
    SanctionedAmount: float = Field(..., example=5000000.0)
    OutstandingPrincipal: float = Field(..., example=4250000.0)
    InterestRate: float = Field(..., example=8.5)
    TenureMonths: int = Field(..., example=240)
    RemainingTenureMonths: int = Field(..., example=195)
    EMIAmount: float = Field(..., example=43391.0)
    NextDueDate: str = Field(..., example="2026-09-10")
    Status: str = Field(default="ACTIVE", example="ACTIVE")


class LoanInquiryResponse(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    Loans: List[LoanAccountModel]


class AmortizationScheduleItem(BaseModel):
    InstallmentNo: int = Field(..., example=1)
    DueDate: str = Field(..., example="2026-09-10")
    PrincipalComponent: float = Field(..., example=13308.0)
    InterestComponent: float = Field(..., example=30083.0)
    TotalInstallment: float = Field(..., example=43391.0)
    EndingBalance: float = Field(..., example=4236692.0)


class LoanScheduleResponse(BaseModel):
    LoanAccountNumber: str = Field(..., example="LN1010000001")
    InterestRate: float = Field(..., example=8.5)
    Schedule: List[AmortizationScheduleItem]


class LoanApplyRequest(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    LoanType: str = Field(..., example="HOME_LOAN", description="HOME_LOAN, AUTO_LOAN, PERSONAL_LOAN")
    RequestedAmount: float = Field(..., example=3000000.0)
    TenureMonths: int = Field(..., example=180)
    MonthlyIncome: float = Field(..., example=120000.0)
    BranchCode: Optional[str] = Field(default="001", example="001")


class LoanApplyResponse(BaseModel):
    ApplicationNumber: str = Field(..., example="LNAPP20260904001")
    Status: str = Field(default="IN_REVIEW", example="IN_REVIEW")
    EstimatedEMI: float = Field(..., example=29570.0)
    Message: str = Field(default="Loan application received successfully", example="Loan application received successfully")


# --- Extra Custom APIs: Deposits ---
class DepositAccountModel(BaseModel):
    DepositAccountNumber: str = Field(..., example="FD1010000001")
    DepositType: str = Field(..., example="FIXED_DEPOSIT", description="FIXED_DEPOSIT or RECURRING_DEPOSIT")
    PrincipalAmount: float = Field(..., example=200000.0)
    InterestRate: float = Field(..., example=7.25)
    MaturityAmount: float = Field(..., example=231800.0)
    DepositDate: str = Field(..., example="2025-09-04")
    MaturityDate: str = Field(..., example="2027-09-04")
    InterestPayout: str = Field(default="ON_MATURITY", example="ON_MATURITY")
    AutoRenewal: bool = Field(default=True, example=True)
    Status: str = Field(default="ACTIVE", example="ACTIVE")


class DepositInquiryResponse(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    Deposits: List[DepositAccountModel]


class DepositOpenRequest(BaseModel):
    CustomerId: str = Field(..., example="CIF100001")
    DebitAccountNumber: str = Field(..., example="101000000001")
    DepositType: str = Field(default="FIXED_DEPOSIT", example="FIXED_DEPOSIT")
    Amount: float = Field(..., example=100000.0)
    TenureMonths: int = Field(..., example=12)
    InterestPayout: Optional[str] = Field(default="ON_MATURITY", example="ON_MATURITY")
    AutoRenewal: Optional[bool] = Field(default=True, example=True)


class DepositOpenResponse(BaseModel):
    DepositAccountNumber: str = Field(..., example="FD1010000099")
    PrincipalAmount: float = Field(..., example=100000.0)
    InterestRate: float = Field(..., example=7.1)
    MaturityAmount: float = Field(..., example=107300.0)
    MaturityDate: str = Field(..., example="2027-09-04")
    Status: str = Field(default="ACTIVE", example="ACTIVE")
    Message: str = Field(default="Term Deposit opened successfully", example="Term Deposit opened successfully")


# --- Extra Custom APIs: Payments / Transfers ---
class FundTransferRequest(BaseModel):
    DebtorAccount: str = Field(..., example="101000000001")
    CreditorAccount: str = Field(..., example="202000000002")
    BeneficiaryName: str = Field(..., example="Jane Doe")
    IFSC: Optional[str] = Field(default="OBDX0000001", example="OBDX0000001")
    Amount: float = Field(..., example=5000.0)
    Currency: Optional[str] = Field(default="INR", example="INR")
    PaymentMode: str = Field(default="IMPS", example="IMPS", description="INTERNAL, IMPS, NEFT, RTGS")
    Remarks: Optional[str] = Field(default="Monthly Rent", example="Monthly Rent")


class FundTransferResponse(BaseModel):
    TransactionReference: str = Field(..., example="FT20260904123456")
    Status: str = Field(default="SUCCESS", example="SUCCESS")
    DebtorAccount: str = Field(..., example="101000000001")
    Amount: float = Field(..., example=5000.0)
    Currency: str = Field(default="INR", example="INR")
    Timestamp: str = Field(..., example="2026-09-04T15:30:00")
    UTR: str = Field(..., example="UTR8839201928")
    Message: str = Field(default="Funds transferred successfully", example="Funds transferred successfully")

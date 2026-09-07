import asyncio
from typing import Any, Callable, Dict, Optional
from fastapi import APIRouter, Request, Response, Body, Query, Path
from app.config import config_manager, dict_to_xml
import app.generators_v2 as gen2
import app.models_v2 as m2

router_v2 = APIRouter(prefix="/api/v2")


async def process_v2_response(
    request: Request,
    endpoint_key: str,
    root_tag: str,
    random_generator: Optional[Callable[..., Dict[str, Any]]] = None,
    gen_kwargs: Optional[Dict[str, Any]] = None
) -> Response:
    cfg = config_manager.get_endpoint_config(endpoint_key)
    
    # 1. Latency simulation
    delay_ms = cfg.get("delay_ms", 0)
    if delay_ms > 0:
        await asyncio.sleep(delay_ms / 1000.0)

    # 2. Determine response mode
    mode = cfg.get("mode", "static")
    status_code = cfg.get("status_code", 200)

    # Check Accept / Content-Type headers
    accept_header = request.headers.get("accept", "").lower()
    content_type_header = request.headers.get("content-type", "").lower()
    wants_xml = "application/xml" in accept_header or "text/xml" in accept_header or ("application/xml" in content_type_header and "application/json" not in accept_header)

    # 3. Handle Error Mode
    if mode == "error":
        err_cfg = cfg.get("error", {})
        err_code = err_cfg.get("code", "BCB-001")
        err_desc = err_cfg.get("description", "Resource Not Found")
        err_sev = err_cfg.get("severity", "ERROR")
        err_status = err_cfg.get("status_code", status_code if status_code >= 400 else 400)
        
        err_dict = {
            "ErrorCode": err_code,
            "ErrorDescription": err_desc,
            "Severity": err_sev
        }

        if wants_xml:
            xml_content = dict_to_xml("ErrorResponse", err_dict)
            return Response(content=xml_content, status_code=err_status, media_type="application/xml")
        else:
            import json
            return Response(content=json.dumps(err_dict, indent=2), status_code=err_status, media_type="application/json")

    # 4. Generate Body Data
    if mode == "random" and random_generator:
        data = random_generator(**(gen_kwargs or {}))
    else:
        # Static mode
        if "static_xml" in cfg and wants_xml:
            return Response(content=cfg["static_xml"], status_code=status_code, media_type="application/xml")
        data = cfg.get("data", {})
        if not data and random_generator:
            data = random_generator(**(gen_kwargs or {}))

    # 5. Return response (JSON by default, XML if requested)
    if wants_xml:
        xml_content = dict_to_xml(root_tag, data)
        return Response(content=xml_content, status_code=status_code, media_type="application/xml")
    else:
        import json
        return Response(content=json.dumps(data, indent=2), status_code=status_code, media_type="application/json")


# ==========================================
# 1. RPM & OBDX Services (Docs YAMLs)
# ==========================================

@router_v2.get(
    "/products/businessproducts",
    tags=["v2 - OBDX/RPM Product Services"],
    summary="Get Business Products Catalog",
    description="Get all valid business products, preferences, currencies, scorecard rules, and attributes from RPM Aggregate Service.",
    response_model=m2.BusProdAggregateServiceModelCollection
)
async def get_business_products(
    request: Request,
    productType: Optional[str] = Query(None, description="Product type (e.g. LOAN, SAVINGS, TERM_DEPOSIT, CURRENT)"),
    channel: Optional[str] = Query("OBDX", description="Originating channel"),
    businessProductCode: Optional[str] = Query(None, description="Business product code (e.g. HL001)")
):
    return await process_v2_response(
        request,
        endpoint_key="v2_business_products",
        root_tag="BusProdAggregateServiceModelCollection",
        random_generator=gen2.generate_random_businessproducts,
        gen_kwargs={"product_type": productType, "channel": channel}
    )


@router_v2.post(
    "/process/initiate",
    tags=["v2 - OBDX/RPM Process Driver"],
    summary="Initiate Application Workflow",
    description="Initiate RPM origination process, generate application number and start workflow task.",
    response_model=m2.ProcessInitiateResponse,
    status_code=201
)
async def process_initiate(
    request: Request,
    payload: Optional[m2.BasicApplicationDetailsModel] = Body(default=None)
):
    ptype = payload.productType if payload else "LOAN"
    channel = payload.channel if payload else "OBDX"
    return await process_v2_response(
        request,
        endpoint_key="v2_process_initiate",
        root_tag="ProcessInitiateResponse",
        random_generator=gen2.generate_random_process_initiate,
        gen_kwargs={"ptype": ptype, "channel": channel}
    )


@router_v2.post(
    "/process/submit",
    tags=["v2 - OBDX/RPM Process Driver"],
    summary="Save / Submit External Application",
    description="Save or submit completed application with domain-specific applicant and product details.",
    response_model=m2.SubmitExtSystemResponse,
    status_code=201
)
async def process_submit(
    request: Request,
    payload: Optional[m2.SubmitExtSystemRequest] = Body(default=None)
):
    app_no = payload.applicationNumber if payload else None
    return await process_v2_response(
        request,
        endpoint_key="v2_process_submit",
        root_tag="SubmitExtSystemResponse",
        random_generator=gen2.generate_random_process_submit,
        gen_kwargs={"app_no": app_no}
    )


@router_v2.get(
    "/process/getData/{applicationNo}",
    tags=["v2 - OBDX/RPM Process Driver"],
    summary="Get Application Data",
    description="Retrieve application data and flow state for a specific application number.",
    response_model=m2.SubmitExtSystemRequest
)
async def process_get_data(
    request: Request,
    applicationNo: str = Path(..., description="Application Number")
):
    return await process_v2_response(
        request,
        endpoint_key="v2_process_get_data",
        root_tag="SubmitExtSystem",
        random_generator=gen2.generate_random_process_get_data,
        gen_kwargs={"app_no": applicationNo}
    )


@router_v2.get(
    "/process/getDocumentList",
    tags=["v2 - OBDX/RPM Process Driver"],
    summary="Get Application Document Checklist",
    description="Retrieve list of mandatory and optional documents required for application or product.",
    response_model=m2.DocumentCollection
)
async def process_get_document_list(
    request: Request,
    applicationNo: Optional[str] = Query(None, description="Application Number"),
    businessProductCode: Optional[str] = Query(None, description="Business Product Code"),
    productType: Optional[str] = Query("LOAN", description="Product Type")
):
    return await process_v2_response(
        request,
        endpoint_key="v2_process_document_list",
        root_tag="DocumentCollection",
        random_generator=gen2.generate_random_document_list,
        gen_kwargs={"app_no": applicationNo, "product_type": productType}
    )


@router_v2.get(
    "/inquiry/applicationsList",
    tags=["v2 - OBDX/RPM Inquiry Services"],
    summary="Filter & Search Applications List",
    description="Query applications with filters (dates, application number, product type, mobile, branch, channel) and pagination.",
    response_model=m2.ApplicationsListResponse
)
async def inquiry_applications_list(
    request: Request,
    fromDate: Optional[str] = Query(None, description="From Date (YYYY-MM-DD)"),
    toDate: Optional[str] = Query(None, description="To Date (YYYY-MM-DD)"),
    applicationNo: Optional[str] = Query(None, description="Application number"),
    processRefNo: Optional[str] = Query(None, description="Process Reference Number"),
    productType: Optional[str] = Query(None, description="Product Type"),
    custName: Optional[str] = Query(None, description="Customer Name"),
    custMobile: Optional[str] = Query(None, description="Customer Mobile"),
    channel: str = Query("OBDX", description="Channel"),
    offset: int = Query(0, description="Offset"),
    limit: int = Query(10, description="Limit")
):
    return await process_v2_response(
        request,
        endpoint_key="v2_inquiry_applications_list",
        root_tag="ApplicationsListResponse",
        random_generator=gen2.generate_random_applications_list,
        gen_kwargs={"offset": offset, "limit": limit}
    )


# ==========================================
# 2. Next-Gen Banking Custom APIs
# ==========================================

# --- Account 360 & Info ---
@router_v2.get(
    "/accounts/{accountId}/info",
    tags=["v2 - Accounts & Statements"],
    summary="Account 360 Information (GET)",
    description="Comprehensive 360-degree account view including balances, interest rate, lien, IFSC, branch, and status.",
    response_model=m2.AccountInfo360Response
)
async def get_account_info_360(
    request: Request,
    accountId: str = Path(..., description="Account ID / Number")
):
    return await process_v2_response(
        request,
        endpoint_key="v2_account_info_360",
        root_tag="AccountInfo360Response",
        random_generator=gen2.generate_random_account_info_360,
        gen_kwargs={"acc_id": accountId}
    )


@router_v2.post(
    "/accounts/info",
    tags=["v2 - Accounts & Statements"],
    summary="Account 360 Information (POST)",
    description="Post-based inquiry for Account 360 information.",
    response_model=m2.AccountInfo360Response
)
async def post_account_info_360(
    request: Request,
    payload: Optional[Dict[str, Any]] = Body(default=None)
):
    acc_id = payload.get("AccountId") or payload.get("AccountNumber") if payload else None
    return await process_v2_response(
        request,
        endpoint_key="v2_account_info_360",
        root_tag="AccountInfo360Response",
        random_generator=gen2.generate_random_account_info_360,
        gen_kwargs={"acc_id": acc_id}
    )


# --- Account Statements ---
@router_v2.get(
    "/accounts/{accountId}/statements",
    tags=["v2 - Accounts & Statements"],
    summary="Account Statement & Transactions (GET)",
    description="Itemized transaction history, running balances, opening/closing balances, and pagination metadata.",
    response_model=m2.AccountStatementResponse
)
async def get_account_statement(
    request: Request,
    accountId: str = Path(..., description="Account ID / Number"),
    fromDate: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    toDate: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
):
    return await process_v2_response(
        request,
        endpoint_key="v2_account_statement",
        root_tag="AccountStatementResponse",
        random_generator=gen2.generate_random_account_statement,
        gen_kwargs={"acc_id": accountId, "from_date": fromDate, "to_date": toDate}
    )


@router_v2.post(
    "/accounts/statements",
    tags=["v2 - Accounts & Statements"],
    summary="Account Statement & Transactions (POST)",
    description="Post-based statement inquiry with date range filter.",
    response_model=m2.AccountStatementResponse
)
async def post_account_statement(
    request: Request,
    payload: Optional[Dict[str, Any]] = Body(default=None)
):
    acc_id = payload.get("AccountId") or payload.get("AccountNumber") if payload else None
    from_date = payload.get("FromDate") if payload else None
    to_date = payload.get("ToDate") if payload else None
    return await process_v2_response(
        request,
        endpoint_key="v2_account_statement",
        root_tag="AccountStatementResponse",
        random_generator=gen2.generate_random_account_statement,
        gen_kwargs={"acc_id": acc_id, "from_date": from_date, "to_date": to_date}
    )


# --- Loans Management ---
@router_v2.get(
    "/loans/accounts",
    tags=["v2 - Loans Management"],
    summary="Customer Loans Portfolio (GET)",
    description="Retrieve all active loan accounts, sanctioned amounts, outstanding balances, EMIs, and interest rates.",
    response_model=m2.LoanInquiryResponse
)
async def get_loans_portfolio(
    request: Request,
    customerId: Optional[str] = Query(None, description="Customer CIF ID")
):
    return await process_v2_response(
        request,
        endpoint_key="v2_loans_portfolio",
        root_tag="LoanInquiryResponse",
        random_generator=gen2.generate_random_loan_accounts,
        gen_kwargs={"cif": customerId}
    )


@router_v2.post(
    "/loans/inquiry",
    tags=["v2 - Loans Management"],
    summary="Customer Loans Portfolio (POST)",
    description="POST inquiry for customer loans portfolio.",
    response_model=m2.LoanInquiryResponse
)
async def post_loans_inquiry(
    request: Request,
    payload: Optional[Dict[str, Any]] = Body(default=None)
):
    cif = payload.get("CustomerId") if payload else None
    return await process_v2_response(
        request,
        endpoint_key="v2_loans_portfolio",
        root_tag="LoanInquiryResponse",
        random_generator=gen2.generate_random_loan_accounts,
        gen_kwargs={"cif": cif}
    )


@router_v2.get(
    "/loans/{loanId}/schedule",
    tags=["v2 - Loans Management"],
    summary="Loan Repayment Amortization Schedule",
    description="Monthly installment breakdown with principal, interest, and ending balances.",
    response_model=m2.LoanScheduleResponse
)
async def get_loan_schedule(
    request: Request,
    loanId: str = Path(..., description="Loan Account Number")
):
    return await process_v2_response(
        request,
        endpoint_key="v2_loan_schedule",
        root_tag="LoanScheduleResponse",
        random_generator=gen2.generate_random_loan_schedule,
        gen_kwargs={"loan_acc": loanId}
    )


@router_v2.post(
    "/loans/apply",
    tags=["v2 - Loans Management"],
    summary="Apply for Loan",
    description="Submit digital loan origination application and calculate estimated EMI.",
    response_model=m2.LoanApplyResponse,
    status_code=201
)
async def apply_for_loan(
    request: Request,
    payload: m2.LoanApplyRequest = Body(...)
):
    return await process_v2_response(
        request,
        endpoint_key="v2_loan_apply",
        root_tag="LoanApplyResponse",
        random_generator=gen2.generate_random_loan_apply,
        gen_kwargs={
            "cif": payload.CustomerId,
            "loan_type": payload.LoanType,
            "amount": payload.RequestedAmount,
            "tenure": payload.TenureMonths
        }
    )


# --- Term Deposits ---
@router_v2.get(
    "/deposits/accounts",
    tags=["v2 - Deposits (FD/RD)"],
    summary="Customer Deposits Portfolio (GET)",
    description="List active Fixed Deposits (FD) and Recurring Deposits (RD) with maturity proceeds.",
    response_model=m2.DepositInquiryResponse
)
async def get_deposits_portfolio(
    request: Request,
    customerId: Optional[str] = Query(None, description="Customer CIF ID")
):
    return await process_v2_response(
        request,
        endpoint_key="v2_deposits_portfolio",
        root_tag="DepositInquiryResponse",
        random_generator=gen2.generate_random_deposit_accounts,
        gen_kwargs={"cif": customerId}
    )


@router_v2.post(
    "/deposits/inquiry",
    tags=["v2 - Deposits (FD/RD)"],
    summary="Customer Deposits Portfolio (POST)",
    description="POST inquiry for customer term deposit portfolio.",
    response_model=m2.DepositInquiryResponse
)
async def post_deposits_inquiry(
    request: Request,
    payload: Optional[Dict[str, Any]] = Body(default=None)
):
    cif = payload.get("CustomerId") if payload else None
    return await process_v2_response(
        request,
        endpoint_key="v2_deposits_portfolio",
        root_tag="DepositInquiryResponse",
        random_generator=gen2.generate_random_deposit_accounts,
        gen_kwargs={"cif": cif}
    )


@router_v2.post(
    "/deposits/open",
    tags=["v2 - Deposits (FD/RD)"],
    summary="Open New Term Deposit",
    description="Instantly create a new Fixed or Recurring deposit with automated maturity calculation.",
    response_model=m2.DepositOpenResponse,
    status_code=201
)
async def open_term_deposit(
    request: Request,
    payload: m2.DepositOpenRequest = Body(...)
):
    return await process_v2_response(
        request,
        endpoint_key="v2_deposit_open",
        root_tag="DepositOpenResponse",
        random_generator=gen2.generate_random_deposit_open,
        gen_kwargs={
            "cif": payload.CustomerId,
            "amount": payload.Amount,
            "tenure": payload.TenureMonths
        }
    )


# --- Payments & Fund Transfers ---
@router_v2.post(
    "/payments/transfer",
    tags=["v2 - Payments & Transfers"],
    summary="Execute Fund Transfer",
    description="Execute immediate fund transfer via INTERNAL, IMPS, NEFT, or RTGS channels.",
    response_model=m2.FundTransferResponse,
    status_code=200
)
async def execute_fund_transfer(
    request: Request,
    payload: m2.FundTransferRequest = Body(...)
):
    return await process_v2_response(
        request,
        endpoint_key="v2_fund_transfer",
        root_tag="FundTransferResponse",
        random_generator=gen2.generate_random_fund_transfer,
        gen_kwargs={
            "debtor": payload.DebtorAccount,
            "creditor": payload.CreditorAccount,
            "amount": payload.Amount,
            "mode": payload.PaymentMode
        }
    )

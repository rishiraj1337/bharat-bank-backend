import asyncio
from typing import Any, Callable, Dict, Optional
from fastapi import APIRouter, Request, Response, Body, Query, Path
from app.config import config_manager, dict_to_xml
import app.generators as gen
import app.generators_v2 as gen2
import app.generators_v3 as gen3
import app.models_v3 as m3

router_v3 = APIRouter(prefix="/api/v3")


async def process_v3_response(
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
    wants_xml = "application/xml" in accept_header or "text/xml" in accept_header or (
        "application/xml" in content_type_header and "application/json" not in accept_header
    )

    # 3. Handle Error Mode
    if mode == "error":
        err_cfg = cfg.get("error", {})
        err_code = err_cfg.get("code", "BCB-001")
        err_desc = err_cfg.get("description", "Customer or Resource Not Found")
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

    # 5. Return response
    if wants_xml:
        xml_content = dict_to_xml(root_tag, data)
        return Response(content=xml_content, status_code=status_code, media_type="application/xml")
    else:
        import json
        return Response(content=json.dumps(data, indent=2), status_code=status_code, media_type="application/json")


# ==========================================================
# 1. Customer & Account Information (Enriched 360)
# ==========================================================

@router_v3.post(
    "/customers/accounts/inquiry",
    tags=["v3 - Customers & Accounts"],
    summary="Customer Account Inquiry (Full 360° View)",
    description="Comprehensive portfolio inquiry returning customer profile, active accounts, balances, IFSC, lien holds, joint holders, nominees, and linked cards.",
    response_model=m3.CustomerAccountInquiryResponseV3
)
async def v3_customer_account_inquiry(
    request: Request,
    payload: Optional[m3.CustomerAccountInquiryRequestV3] = Body(default=None)
):
    cif = payload.CustomerId if payload else None
    return await process_v3_response(
        request,
        endpoint_key="v3_customer_account_inquiry",
        root_tag="CustomerAccountInquiryResponse",
        random_generator=gen3.generate_v3_customer_account_inquiry,
        gen_kwargs={"req_cif": cif}
    )


@router_v3.post(
    "/customers/accounts/basic-inquiry",
    tags=["v3 - Customers & Accounts"],
    summary="Customer Account Basic Inquiry",
    description="Lightweight endpoint returning high-level customer information and available balances.",
    response_model=m3.CustomerAccountBasicInquiryResponseV3
)
async def v3_customer_account_basic_inquiry(
    request: Request,
    payload: Optional[m3.CustomerAccountBasicInquiryRequestV3] = Body(default=None)
):
    cif = payload.CustomerId if payload else None
    return await process_v3_response(
        request,
        endpoint_key="v3_customer_account_basic_inquiry",
        root_tag="CustomerAccountBasicInquiryResponse",
        random_generator=gen3.generate_v3_customer_account_basic,
        gen_kwargs={"req_cif": cif}
    )


@router_v3.post(
    "/accounts/details/inquiry",
    tags=["v3 - Customers & Accounts"],
    summary="Account Details Inquiry (POST)",
    description="Retrieves account metadata, product configuration, linked cards, related parties, and nominee details.",
    response_model=m3.AccountDetailsInquiryResponseV3
)
async def v3_account_details_inquiry(
    request: Request,
    payload: Optional[m3.AccountDetailsInquiryRequestV3] = Body(default=None)
):
    acc = payload.AccountId if payload else None
    return await process_v3_response(
        request,
        endpoint_key="v3_account_details_inquiry",
        root_tag="AccountDetailsInquiryResponse",
        random_generator=gen3.generate_v3_account_details,
        gen_kwargs={"req_acc": acc}
    )


@router_v3.get(
    "/accounts/{accountId}/details",
    tags=["v3 - Customers & Accounts"],
    summary="Account Details Inquiry (GET Alias)",
    response_model=m3.AccountDetailsInquiryResponseV3
)
async def v3_account_details_get(
    request: Request,
    accountId: str = Path(..., description="12-digit CBS Account Number")
):
    return await process_v3_response(
        request,
        endpoint_key="v3_account_details_inquiry",
        root_tag="AccountDetailsInquiryResponse",
        random_generator=gen3.generate_v3_account_details,
        gen_kwargs={"req_acc": accountId}
    )


# ==========================================================
# 2. Account Actions & Statements
# ==========================================================

@router_v3.post(
    "/accounts/opening-balance",
    tags=["v3 - Accounts Management"],
    summary="Account Opening Balance",
    description="Fetches the historical ledger opening balance of an account as of a specified date.",
    response_model=m3.AccountOpeningBalanceResponseV3
)
async def v3_account_opening_balance(
    request: Request,
    payload: Optional[m3.AccountOpeningBalanceRequestV3] = Body(default=None)
):
    acc = payload.AccountId if payload else None
    as_on = payload.AsOnDate if payload else "2026-09-01"
    return await process_v3_response(
        request,
        endpoint_key="v3_account_opening_balance",
        root_tag="AccountOpeningBalanceResponse",
        random_generator=gen.generate_random_opening_balance,
        gen_kwargs={"req_acc": acc, "as_on": as_on}
    )


@router_v3.post(
    "/accounts/freeze",
    tags=["v3 - Accounts Management"],
    summary="Account Freeze",
    description="Places a DEBIT, CREDIT, FULL, or LIEN administrative freeze on an account.",
    response_model=m3.StatusResponseV3
)
async def v3_account_freeze(
    request: Request,
    payload: Optional[m3.AccountFreezeRequestV3] = Body(default=None)
):
    acc = payload.AccountId if payload else None
    freeze_type = payload.FreezeType if payload else "DEBIT"
    return await process_v3_response(
        request,
        endpoint_key="v3_account_freeze",
        root_tag="StatusResponse",
        random_generator=gen.generate_random_freeze,
        gen_kwargs={"req_acc": acc, "freeze_type": freeze_type}
    )


@router_v3.post(
    "/accounts/unfreeze",
    tags=["v3 - Accounts Management"],
    summary="Account Unfreeze",
    description="Removes administrative freeze or restriction holds from an account.",
    response_model=m3.StatusResponseV3
)
async def v3_account_unfreeze(
    request: Request,
    payload: Optional[m3.AccountUnfreezeRequestV3] = Body(default=None)
):
    acc = payload.AccountId if payload else None
    return await process_v3_response(
        request,
        endpoint_key="v3_account_unfreeze",
        root_tag="StatusResponse",
        random_generator=gen.generate_random_unfreeze,
        gen_kwargs={"req_acc": acc}
    )


@router_v3.post(
    "/accounts/statements",
    tags=["v3 - Accounts Management"],
    summary="Account Statement & Transactions (POST)",
    description="Itemized account statement with transaction ledger, debits/credits, running balances, and pagination metadata.",
    response_model=m3.AccountStatementResponseV3
)
async def v3_account_statements(
    request: Request,
    payload: Optional[m3.AccountStatementRequestV3] = Body(default=None)
):
    acc = payload.AccountId if payload else None
    from_date = payload.FromDate if payload else None
    to_date = payload.ToDate if payload else None
    offset = payload.Offset if payload else 0
    limit = payload.Limit if payload else 10
    return await process_v3_response(
        request,
        endpoint_key="v3_account_statements",
        root_tag="AccountStatementResponse",
        random_generator=gen3.generate_v3_account_statements,
        gen_kwargs={"req_acc": acc, "from_date": from_date, "to_date": to_date, "offset": offset, "limit": limit}
    )


@router_v3.get(
    "/accounts/{accountId}/statements",
    tags=["v3 - Accounts Management"],
    summary="Account Statement & Transactions (GET Alias)",
    response_model=m3.AccountStatementResponseV3
)
async def v3_account_statements_get(
    request: Request,
    accountId: str = Path(..., description="12-digit CBS Account Number"),
    fromDate: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    toDate: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    offset: int = Query(0, description="Offset"),
    limit: int = Query(10, description="Limit")
):
    return await process_v3_response(
        request,
        endpoint_key="v3_account_statements",
        root_tag="AccountStatementResponse",
        random_generator=gen3.generate_v3_account_statements,
        gen_kwargs={"req_acc": accountId, "from_date": fromDate, "to_date": toDate, "offset": offset, "limit": limit}
    )


# ==========================================================
# 3. Cards Management
# ==========================================================

@router_v3.post(
    "/cards/status/update",
    tags=["v3 - Cards Management"],
    summary="Card Status Update",
    description="Updates card status (ACTIVE, BLOCKED, HOTLISTED, CLOSED).",
    response_model=m3.StatusResponseV3
)
async def v3_card_status_update(
    request: Request,
    payload: Optional[m3.CardStatusUpdateRequestV3] = Body(default=None)
):
    card = payload.CardNumber if payload else None
    new_status = payload.NewCardStatus if payload else "BLOCKED"
    return await process_v3_response(
        request,
        endpoint_key="v3_card_status_update",
        root_tag="StatusResponse",
        random_generator=gen.generate_random_card_update,
        gen_kwargs={"req_card": card, "new_status": new_status}
    )


@router_v3.post(
    "/cards/inquiry",
    tags=["v3 - Cards Management"],
    summary="Cards Inquiry",
    description="Inquires all debit and credit cards linked to an account.",
    response_model=m3.CardInquiryResponseV3
)
async def v3_card_inquiry(
    request: Request,
    payload: Optional[m3.CardInquiryRequestV3] = Body(default=None)
):
    acc = payload.AccountId if payload else "101000000001"
    return await process_v3_response(
        request,
        endpoint_key="v3_card_inquiry",
        root_tag="CardInquiryResponse",
        random_generator=lambda: {
            "AccountId": acc,
            "Cards": {
                "Card": [
                    {"CardNumber": "XXXXXX1234", "CardType": "DEBIT", "Status": "ACTIVE", "ExpiryDate": "2029-12-31"},
                    {"CardNumber": "XXXXXX5678", "CardType": "VIRTUAL_DEBIT", "Status": "ACTIVE", "ExpiryDate": "2030-06-30"}
                ]
            }
        }
    )


# ==========================================================
# 4. Cheque Operations
# ==========================================================

@router_v3.post(
    "/cheques/issued/summary",
    tags=["v3 - Cheques Operations"],
    summary="Cheque Issued Summary",
    response_model=m3.ChequeIssuedSummaryResponseV3
)
async def v3_cheque_issued_summary(
    request: Request,
    payload: Optional[m3.ChequeIssuedSummaryRequestV3] = Body(default=None)
):
    cif = payload.CustomerId if payload else None
    return await process_v3_response(
        request,
        endpoint_key="v3_cheque_issued_summary",
        root_tag="ChequeIssuedSummaryResponse",
        random_generator=gen.generate_random_cheque_issued_summary,
        gen_kwargs={"cif": cif}
    )


@router_v3.post(
    "/cheques/issued/details",
    tags=["v3 - Cheques Operations"],
    summary="Cheque Issued Detail",
    response_model=m3.ChequeIssuedDetailResponseV3
)
async def v3_cheque_issued_details(
    request: Request,
    payload: Optional[m3.ChequeIssuedDetailRequestV3] = Body(default=None)
):
    cif = payload.CustomerId if payload else None
    return await process_v3_response(
        request,
        endpoint_key="v3_cheque_issued_details",
        root_tag="ChequeIssuedDetailResponse",
        random_generator=gen.generate_random_cheque_issued_details,
        gen_kwargs={"cif": cif}
    )


@router_v3.post(
    "/cheques/deposited/summary",
    tags=["v3 - Cheques Operations"],
    summary="Cheque Deposited Summary",
    response_model=m3.ChequeDepositedSummaryResponseV3
)
async def v3_cheque_deposited_summary(
    request: Request,
    payload: Optional[m3.ChequeDepositedSummaryRequestV3] = Body(default=None)
):
    cif = payload.CustomerId if payload else None
    return await process_v3_response(
        request,
        endpoint_key="v3_cheque_deposited_summary",
        root_tag="ChequeDepositedSummaryResponse",
        random_generator=gen.generate_random_cheque_deposited_summary,
        gen_kwargs={"cif": cif}
    )


@router_v3.post(
    "/cheques/deposited/details",
    tags=["v3 - Cheques Operations"],
    summary="Cheque Deposited Detail",
    response_model=m3.ChequeDepositedDetailResponseV3
)
async def v3_cheque_deposited_details(
    request: Request,
    payload: Optional[m3.ChequeDepositedDetailRequestV3] = Body(default=None)
):
    cif = payload.CustomerId if payload else None
    return await process_v3_response(
        request,
        endpoint_key="v3_cheque_deposited_details",
        root_tag="ChequeDepositedDetailResponse",
        random_generator=gen.generate_random_cheque_deposited_details,
        gen_kwargs={"cif": cif}
    )


@router_v3.post(
    "/cheques/status/inquiry",
    tags=["v3 - Cheques Operations"],
    summary="Passed and Stopped Cheque Inquiry",
    response_model=m3.ChequeStatusResponseV3
)
async def v3_cheque_status_inquiry(
    request: Request,
    payload: Optional[m3.ChequeStatusRequestV3] = Body(default=None)
):
    acc = payload.AccountId if payload else None
    chq = payload.ChequeNumber if payload else None
    return await process_v3_response(
        request,
        endpoint_key="v3_cheque_status_inquiry",
        root_tag="ChequeStatusResponse",
        random_generator=gen.generate_random_cheque_status,
        gen_kwargs={"acc": acc, "chq": chq}
    )


@router_v3.post(
    "/cheques/leaves/status",
    tags=["v3 - Cheques Operations"],
    summary="Cheque Leaves Status",
    response_model=m3.ChequeLeavesStatusResponseV3
)
async def v3_cheque_leaves_status(
    request: Request,
    payload: Optional[m3.ChequeLeavesStatusRequestV3] = Body(default=None)
):
    acc = payload.AccountId if payload else None
    return await process_v3_response(
        request,
        endpoint_key="v3_cheque_leaves_status",
        root_tag="ChequeLeavesStatusResponse",
        random_generator=gen.generate_random_cheque_leaves_status,
        gen_kwargs={"acc": acc}
    )


@router_v3.post(
    "/cheques/stop-payment",
    tags=["v3 - Cheques Operations"],
    summary="Stop Cheque Payment",
    response_model=m3.StatusResponseV3
)
async def v3_cheque_stop_payment(
    request: Request,
    payload: m3.ChequeStopPaymentRequestV3 = Body(...)
):
    return await process_v3_response(
        request,
        endpoint_key="v3_cheque_stop_payment",
        root_tag="StatusResponse",
        random_generator=lambda: {
            "Status": "SUCCESS",
            "ReferenceNumber": "STP123456",
            "Message": f"Stop payment applied successfully for Cheque {payload.ChequeNumber}"
        }
    )


# ==========================================================
# 5. Certificates & Compliance
# ==========================================================

@router_v3.post(
    "/certificates/interest",
    tags=["v3 - Certificates & Compliance"],
    summary="Interest Certificate",
    response_model=m3.InterestCertificateResponseV3
)
async def v3_interest_certificate(
    request: Request,
    payload: Optional[m3.InterestCertificateRequestV3] = Body(default=None)
):
    cif = payload.CustomerId if payload else None
    year = payload.FinancialYear if payload else "2026"
    return await process_v3_response(
        request,
        endpoint_key="v3_interest_certificate",
        root_tag="InterestCertificateResponse",
        random_generator=gen.generate_random_interest_cert,
        gen_kwargs={"cif": cif, "year": year}
    )


@router_v3.post(
    "/certificates/tds",
    tags=["v3 - Certificates & Compliance"],
    summary="TDS Certificate",
    response_model=m3.TDSCertificateResponseV3
)
async def v3_tds_certificate(
    request: Request,
    payload: Optional[m3.TDSCertificateRequestV3] = Body(default=None)
):
    cif = payload.CustomerId if payload else None
    year = payload.FinancialYear if payload else "2026"
    return await process_v3_response(
        request,
        endpoint_key="v3_tds_certificate",
        root_tag="TDSCertificateResponse",
        random_generator=gen.generate_random_tds_cert,
        gen_kwargs={"cif": cif, "year": year}
    )


# ==========================================================
# 6. Lockers & Customer Validation
# ==========================================================

@router_v3.post(
    "/lockers/inquiry",
    tags=["v3 - Lockers & Utilities"],
    summary="Locker Inquiry",
    response_model=m3.LockerInquiryResponseV3
)
async def v3_locker_inquiry(
    request: Request,
    payload: Optional[m3.LockerInquiryRequestV3] = Body(default=None)
):
    branch = payload.BranchCode if payload else "001"
    return await process_v3_response(
        request,
        endpoint_key="v3_locker_inquiry",
        root_tag="LockerInquiryResponse",
        random_generator=gen.generate_random_locker_inquiry,
        gen_kwargs={"branch": branch}
    )


@router_v3.post(
    "/customers/mobile/validate",
    tags=["v3 - Customers & Accounts"],
    summary="Mobile Validation",
    response_model=m3.MobileValidationResponseV3
)
async def v3_mobile_validation(
    request: Request,
    payload: Optional[m3.MobileValidationRequestV3] = Body(default=None)
):
    cif = payload.CustomerId if payload else None
    mobile = payload.MobileNumber if payload else None
    return await process_v3_response(
        request,
        endpoint_key="v3_mobile_validation",
        root_tag="MobileValidationResponse",
        random_generator=gen.generate_random_mobile_validation,
        gen_kwargs={"cif": cif, "mobile": mobile}
    )


# ==========================================================
# 7. Loans Management & Amortization
# ==========================================================

@router_v3.post(
    "/loans/inquiry",
    tags=["v3 - Loans Management"],
    summary="Customer Loans Portfolio Inquiry (POST)",
    response_model=m3.LoanInquiryResponseV3
)
async def v3_loans_inquiry(
    request: Request,
    payload: Optional[m3.LoanInquiryRequestV3] = Body(default=None)
):
    cif = payload.CustomerId if payload else None
    return await process_v3_response(
        request,
        endpoint_key="v3_loans_inquiry",
        root_tag="LoanInquiryResponse",
        random_generator=gen3.generate_v3_loans_inquiry,
        gen_kwargs={"req_cif": cif}
    )


@router_v3.get(
    "/loans/accounts",
    tags=["v3 - Loans Management"],
    summary="Customer Loans Portfolio (GET Alias)",
    response_model=m3.LoanInquiryResponseV3
)
async def v3_loans_accounts_get(
    request: Request,
    customerId: Optional[str] = Query("CIF100001", description="Customer CIF ID")
):
    return await process_v3_response(
        request,
        endpoint_key="v3_loans_inquiry",
        root_tag="LoanInquiryResponse",
        random_generator=gen3.generate_v3_loans_inquiry,
        gen_kwargs={"req_cif": customerId}
    )


@router_v3.post(
    "/loans/schedule",
    tags=["v3 - Loans Management"],
    summary="Loan Repayment Amortization Schedule (POST)",
    response_model=m3.LoanScheduleResponseV3
)
async def v3_loan_schedule(
    request: Request,
    payload: m3.LoanScheduleRequestV3 = Body(...)
):
    return await process_v3_response(
        request,
        endpoint_key="v3_loan_schedule",
        root_tag="LoanScheduleResponse",
        random_generator=gen3.generate_v3_loan_schedule,
        gen_kwargs={"req_loan": payload.LoanAccountNumber}
    )


@router_v3.get(
    "/loans/{loanId}/schedule",
    tags=["v3 - Loans Management"],
    summary="Loan Repayment Schedule (GET Alias)",
    response_model=m3.LoanScheduleResponseV3
)
async def v3_loan_schedule_get(
    request: Request,
    loanId: str = Path(..., description="Loan Account Number")
):
    return await process_v3_response(
        request,
        endpoint_key="v3_loan_schedule",
        root_tag="LoanScheduleResponse",
        random_generator=gen3.generate_v3_loan_schedule,
        gen_kwargs={"req_loan": loanId}
    )


@router_v3.post(
    "/loans/apply",
    tags=["v3 - Loans Management"],
    summary="Apply for Loan",
    response_model=m3.LoanApplyResponseV3,
    status_code=201
)
async def v3_loan_apply(
    request: Request,
    payload: m3.LoanApplyRequestV3 = Body(...)
):
    return await process_v3_response(
        request,
        endpoint_key="v3_loan_apply",
        root_tag="LoanApplyResponse",
        random_generator=gen2.generate_random_loan_apply,
        gen_kwargs={
            "cif": payload.CustomerId,
            "loan_type": payload.LoanType,
            "amount": payload.RequestedAmount,
            "tenure": payload.TenureMonths
        }
    )


# ==========================================================
# 8. Term Deposits (FD / RD & Pre-closure)
# ==========================================================

@router_v3.post(
    "/deposits/td/inquiry",
    tags=["v3 - Term Deposits (FD/RD)"],
    summary="Customer Term Deposits Inquiry (POST)",
    response_model=m3.TermDepositInquiryResponseV3
)
async def v3_deposits_inquiry(
    request: Request,
    payload: Optional[m3.TermDepositInquiryRequestV3] = Body(default=None)
):
    cif = payload.CustomerId if payload else None
    return await process_v3_response(
        request,
        endpoint_key="v3_deposits_inquiry",
        root_tag="TermDepositInquiryResponse",
        random_generator=gen3.generate_v3_deposits_inquiry,
        gen_kwargs={"req_cif": cif}
    )


@router_v3.get(
    "/deposits/accounts",
    tags=["v3 - Term Deposits (FD/RD)"],
    summary="Customer Term Deposits (GET Alias)",
    response_model=m3.TermDepositInquiryResponseV3
)
async def v3_deposits_accounts_get(
    request: Request,
    customerId: Optional[str] = Query("CIF100001", description="Customer CIF ID")
):
    return await process_v3_response(
        request,
        endpoint_key="v3_deposits_inquiry",
        root_tag="TermDepositInquiryResponse",
        random_generator=gen3.generate_v3_deposits_inquiry,
        gen_kwargs={"req_cif": customerId}
    )


@router_v3.post(
    "/deposits/td/open",
    tags=["v3 - Term Deposits (FD/RD)"],
    summary="Open New Term Deposit",
    response_model=m3.TermDepositOpenResponseV3,
    status_code=201
)
async def v3_deposits_open(
    request: Request,
    payload: m3.TermDepositOpenRequestV3 = Body(...)
):
    return await process_v3_response(
        request,
        endpoint_key="v3_deposit_open",
        root_tag="TermDepositOpenResponse",
        random_generator=gen2.generate_random_deposit_open,
        gen_kwargs={
            "cif": payload.CustomerId,
            "amount": payload.Amount,
            "tenure": payload.TenureMonths
        }
    )


@router_v3.post(
    "/deposits/td/trial-closure",
    tags=["v3 - Term Deposits (FD/RD)"],
    summary="Term Deposit Trial Pre-closure Simulation",
    response_model=m3.TDTrialClosureResponseV3
)
async def v3_td_trial_closure(
    request: Request,
    payload: Optional[m3.TDTrialClosureRequestV3] = Body(default=None)
):
    acc = payload.TDAccountId if payload else None
    return await process_v3_response(
        request,
        endpoint_key="v3_td_trial_closure",
        root_tag="TDTrialClosureResponse",
        random_generator=gen.generate_random_td_trial_closure,
        gen_kwargs={"acc": acc}
    )


# ==========================================================
# 9. Payments, Upcoming Inflows & Transfers
# ==========================================================

@router_v3.post(
    "/payments/upcoming",
    tags=["v3 - Payments & Inflows"],
    summary="Upcoming Scheduled Payments / EMIs",
    response_model=m3.UpcomingPaymentsResponseV3
)
async def v3_upcoming_payments(
    request: Request,
    payload: Optional[m3.UpcomingPaymentsRequestV3] = Body(default=None)
):
    cif = payload.CustomerId if payload else None
    return await process_v3_response(
        request,
        endpoint_key="v3_upcoming_payments",
        root_tag="UpcomingPaymentsResponse",
        random_generator=gen.generate_random_upcoming_payments,
        gen_kwargs={"cif": cif}
    )


@router_v3.post(
    "/income/upcoming",
    tags=["v3 - Payments & Inflows"],
    summary="Upcoming Scheduled Income / Interest Inflows",
    response_model=m3.UpcomingIncomeResponseV3
)
async def v3_upcoming_income(
    request: Request,
    payload: Optional[m3.UpcomingIncomeRequestV3] = Body(default=None)
):
    cif = payload.CustomerId if payload else None
    return await process_v3_response(
        request,
        endpoint_key="v3_upcoming_income",
        root_tag="UpcomingIncomeResponse",
        random_generator=gen.generate_random_upcoming_income,
        gen_kwargs={"cif": cif}
    )


@router_v3.post(
    "/payments/transfer",
    tags=["v3 - Payments & Inflows"],
    summary="Execute Fund Transfer",
    response_model=m3.FundTransferResponseV3
)
async def v3_fund_transfer(
    request: Request,
    payload: m3.FundTransferRequestV3 = Body(...)
):
    return await process_v3_response(
        request,
        endpoint_key="v3_fund_transfer",
        root_tag="FundTransferResponse",
        random_generator=gen2.generate_random_fund_transfer,
        gen_kwargs={
            "debtor": payload.DebtorAccount,
            "creditor": payload.CreditorAccount,
            "amount": payload.Amount,
            "mode": payload.PaymentMode
        }
    )


# ==========================================================
# 10. Oracle OBDX / RPM Origination & Products
# ==========================================================

@router_v3.post(
    "/products/businessproducts",
    tags=["v3 - OBDX / RPM Product & Process"],
    summary="Business Products Catalog Inquiry (POST)",
    description="Inquire maintenance parameters, rules, currency configurations, and fee definitions."
)
async def v3_business_products_post(
    request: Request,
    payload: Optional[m3.BusProdAggregateInquiryRequestV3] = Body(default=None)
):
    ptype = payload.productType if payload else "LOAN"
    channel = payload.channel if payload else "OBDX"
    return await process_v3_response(
        request,
        endpoint_key="v3_business_products",
        root_tag="BusProdAggregateServiceModelCollection",
        random_generator=gen2.generate_random_businessproducts,
        gen_kwargs={"product_type": ptype, "channel": channel}
    )


@router_v3.get(
    "/products/businessproducts",
    tags=["v3 - OBDX / RPM Product & Process"],
    summary="Business Products Catalog (GET Alias)"
)
async def v3_business_products_get(
    request: Request,
    productType: Optional[str] = Query("LOAN", description="Product type"),
    channel: Optional[str] = Query("OBDX", description="Channel")
):
    return await process_v3_response(
        request,
        endpoint_key="v3_business_products",
        root_tag="BusProdAggregateServiceModelCollection",
        random_generator=gen2.generate_random_businessproducts,
        gen_kwargs={"product_type": productType, "channel": channel}
    )


@router_v3.post(
    "/process/initiate",
    tags=["v3 - OBDX / RPM Product & Process"],
    summary="Initiate Application Workflow",
    response_model=m3.ProcessInitiateResponseV3,
    status_code=201
)
async def v3_process_initiate(
    request: Request,
    payload: Optional[m3.ProcessInitiateRequestV3] = Body(default=None)
):
    ptype = payload.productType if payload else "LOAN"
    channel = payload.channel if payload else "OBDX"
    return await process_v3_response(
        request,
        endpoint_key="v3_process_initiate",
        root_tag="ProcessInitiateResponse",
        random_generator=gen2.generate_random_process_initiate,
        gen_kwargs={"ptype": ptype, "channel": channel}
    )


@router_v3.post(
    "/process/submit",
    tags=["v3 - OBDX / RPM Product & Process"],
    summary="Submit Application with Domain Payload",
    response_model=m3.ProcessSubmitResponseV3,
    status_code=201
)
async def v3_process_submit(
    request: Request,
    payload: Optional[m3.ProcessSubmitRequestV3] = Body(default=None)
):
    app_no = payload.applicationNumber if payload else None
    return await process_v3_response(
        request,
        endpoint_key="v3_process_submit",
        root_tag="SubmitExtSystemResponse",
        random_generator=gen2.generate_random_process_submit,
        gen_kwargs={"app_no": app_no}
    )


@router_v3.post(
    "/process/get-data",
    tags=["v3 - OBDX / RPM Product & Process"],
    summary="Get Application Data (POST)"
)
async def v3_process_get_data_post(
    request: Request,
    payload: m3.ProcessGetDataRequestV3 = Body(...)
):
    return await process_v3_response(
        request,
        endpoint_key="v3_process_get_data",
        root_tag="SubmitExtSystem",
        random_generator=gen2.generate_random_process_get_data,
        gen_kwargs={"app_no": payload.applicationNumber}
    )


@router_v3.get(
    "/process/getData/{applicationNo}",
    tags=["v3 - OBDX / RPM Product & Process"],
    summary="Get Application Data (GET Alias)"
)
async def v3_process_get_data_get(
    request: Request,
    applicationNo: str = Path(..., description="Application Number")
):
    return await process_v3_response(
        request,
        endpoint_key="v3_process_get_data",
        root_tag="SubmitExtSystem",
        random_generator=gen2.generate_random_process_get_data,
        gen_kwargs={"app_no": applicationNo}
    )


@router_v3.post(
    "/process/get-document-list",
    tags=["v3 - OBDX / RPM Product & Process"],
    summary="Get Document List (POST)"
)
async def v3_process_get_document_list_post(
    request: Request,
    payload: Optional[m3.ProcessGetDocumentListRequestV3] = Body(default=None)
):
    app_no = payload.applicationNumber if payload else None
    ptype = payload.productType if payload else "LOAN"
    return await process_v3_response(
        request,
        endpoint_key="v3_process_document_list",
        root_tag="DocumentCollection",
        random_generator=gen2.generate_random_document_list,
        gen_kwargs={"app_no": app_no, "product_type": ptype}
    )


@router_v3.get(
    "/process/getDocumentList",
    tags=["v3 - OBDX / RPM Product & Process"],
    summary="Get Document List (GET Alias)"
)
async def v3_process_get_document_list_get(
    request: Request,
    applicationNo: Optional[str] = Query(None),
    productType: Optional[str] = Query("LOAN")
):
    return await process_v3_response(
        request,
        endpoint_key="v3_process_document_list",
        root_tag="DocumentCollection",
        random_generator=gen2.generate_random_document_list,
        gen_kwargs={"app_no": applicationNo, "product_type": productType}
    )


@router_v3.post(
    "/inquiry/applications-list",
    tags=["v3 - OBDX / RPM Product & Process"],
    summary="Filter Applications List (POST)"
)
async def v3_inquiry_applications_list_post(
    request: Request,
    payload: Optional[m3.ApplicationsListInquiryRequestV3] = Body(default=None)
):
    offset = payload.offset if payload else 0
    limit = payload.limit if payload else 10
    return await process_v3_response(
        request,
        endpoint_key="v3_inquiry_applications_list",
        root_tag="ApplicationsListResponse",
        random_generator=gen2.generate_random_applications_list,
        gen_kwargs={"offset": offset, "limit": limit}
    )


@router_v3.get(
    "/inquiry/applicationsList",
    tags=["v3 - OBDX / RPM Product & Process"],
    summary="Filter Applications List (GET Alias)"
)
async def v3_inquiry_applications_list_get(
    request: Request,
    offset: int = Query(0),
    limit: int = Query(10)
):
    return await process_v3_response(
        request,
        endpoint_key="v3_inquiry_applications_list",
        root_tag="ApplicationsListResponse",
        random_generator=gen2.generate_random_applications_list,
        gen_kwargs={"offset": offset, "limit": limit}
    )

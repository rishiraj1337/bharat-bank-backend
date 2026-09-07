import asyncio
from typing import Any, Callable, Dict, Optional
from fastapi import APIRouter, Request, Response, Body, status
from app.config import config_manager, dict_to_xml, wrap_cbs_envelope
import app.generators as gen
import app.models as models

router = APIRouter(prefix="/api/v1", tags=["Core Banking System (CBS) APIs"])


async def process_mock_response(
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

    # Check Accept header
    accept_header = request.headers.get("accept", "").lower()
    content_type_header = request.headers.get("content-type", "").lower()
    wants_json = "application/json" in accept_header or (not accept_header and "application/json" in content_type_header)

    # 3. Handle Error Mode
    if mode == "error":
        err_cfg = cfg.get("error", {})
        err_code = err_cfg.get("code", "BCB-001")
        err_desc = err_cfg.get("description", "Customer Not Found")
        err_sev = err_cfg.get("severity", "ERROR")
        err_status = err_cfg.get("status_code", status_code if status_code >= 400 else 400)
        
        err_dict = {
            "ErrorCode": err_code,
            "ErrorDescription": err_desc,
            "Severity": err_sev
        }

        if wants_json:
            import json
            return Response(
                content=json.dumps(err_dict, indent=2),
                status_code=err_status,
                media_type="application/json"
            )
        else:
            xml_content = dict_to_xml("ErrorResponse", err_dict)
            return Response(
                content=xml_content,
                status_code=err_status,
                media_type="application/xml"
            )

    # 4. Generate Body Data
    if mode == "random" and random_generator:
        data = random_generator(**(gen_kwargs or {}))
    else:
        # Static mode
        if "static_xml" in cfg and not wants_json:
            return Response(
                content=cfg["static_xml"],
                status_code=status_code,
                media_type="application/xml"
            )
        data = cfg.get("data", {})

    # 5. Return JSON or XML response
    if wants_json:
        import json
        return Response(
            content=json.dumps(data, indent=2),
            status_code=status_code,
            media_type="application/json"
        )
    else:
        xml_content = dict_to_xml(root_tag, data)
        return Response(
            content=xml_content,
            status_code=status_code,
            media_type="application/xml"
        )


# --- 1. Customer Account Inquiry ---
@router.post(
    "/customers/accounts/inquiry",
    summary="Customer Account Inquiry",
    response_model=models.CustomerAccountInquiryResponse,
    responses={
        200: {"description": "Customer accounts portfolio and balances"},
        400: {"model": models.ErrorResponse},
        404: {"model": models.ErrorResponse}
    }
)
async def customer_account_inquiry(
    request: Request,
    payload: Optional[models.CustomerAccountInquiryRequest] = Body(default=None)
):
    cif = payload.CustomerId if payload else None
    return await process_mock_response(
        request,
        endpoint_key="customer_account_inquiry",
        root_tag="CustomerAccountInquiryResponse",
        random_generator=gen.generate_random_customer_account_inquiry,
        gen_kwargs={"req_cif": cif}
    )


# --- 2. Customer Account Basic Inquiry ---
@router.post(
    "/customers/accounts/basic-inquiry",
    summary="Customer Account Basic Inquiry",
    response_model=models.CustomerAccountBasicInquiryResponse
)
async def customer_account_basic_inquiry(
    request: Request,
    payload: Optional[models.CustomerAccountBasicInquiryRequest] = Body(default=None)
):
    cif = payload.CustomerId if payload else None
    return await process_mock_response(
        request,
        endpoint_key="customer_account_basic_inquiry",
        root_tag="CustomerAccountBasicInquiryResponse",
        random_generator=gen.generate_random_customer_account_basic,
        gen_kwargs={"req_cif": cif}
    )


# --- 3. Account Details Inquiry ---
@router.post(
    "/accounts/details/inquiry",
    summary="Account Details Inquiry",
    response_model=models.AccountDetailsInquiryResponse
)
async def account_details_inquiry(
    request: Request,
    payload: Optional[models.AccountDetailsInquiryRequest] = Body(default=None)
):
    acc = payload.AccountId if payload else None
    return await process_mock_response(
        request,
        endpoint_key="account_details_inquiry",
        root_tag="AccountDetailsInquiryResponse",
        random_generator=gen.generate_random_account_details,
        gen_kwargs={"req_acc": acc}
    )


# --- 4. Account Opening Balance ---
@router.post(
    "/accounts/opening-balance",
    summary="Account Opening Balance",
    response_model=models.AccountOpeningBalanceResponse
)
async def account_opening_balance(
    request: Request,
    payload: Optional[models.AccountOpeningBalanceRequest] = Body(default=None)
):
    acc = payload.AccountId if payload else None
    as_on = payload.AsOnDate if payload else None
    return await process_mock_response(
        request,
        endpoint_key="account_opening_balance",
        root_tag="AccountOpeningBalanceResponse",
        random_generator=gen.generate_random_opening_balance,
        gen_kwargs={"req_acc": acc, "as_on": as_on}
    )


# --- 5. Account Freeze ---
@router.post(
    "/accounts/freeze",
    summary="Account Freeze",
    response_model=models.StatusResponse
)
async def account_freeze(
    request: Request,
    payload: Optional[models.AccountFreezeRequest] = Body(default=None)
):
    acc = payload.AccountId if payload else None
    freeze_type = payload.FreezeType if payload else "DEBIT"
    return await process_mock_response(
        request,
        endpoint_key="account_freeze",
        root_tag="StatusResponse",
        random_generator=gen.generate_random_freeze,
        gen_kwargs={"req_acc": acc, "freeze_type": freeze_type}
    )


# --- 6. Account Unfreeze ---
@router.post(
    "/accounts/unfreeze",
    summary="Account Unfreeze",
    response_model=models.StatusResponse
)
async def account_unfreeze(
    request: Request,
    payload: Optional[models.AccountUnfreezeRequest] = Body(default=None)
):
    acc = payload.AccountId if payload else None
    return await process_mock_response(
        request,
        endpoint_key="account_unfreeze",
        root_tag="StatusResponse",
        random_generator=gen.generate_random_unfreeze,
        gen_kwargs={"req_acc": acc}
    )


# --- 7. Card Status Update ---
@router.post(
    "/cards/status/update",
    summary="Card Status Update",
    response_model=models.StatusResponse
)
async def card_status_update(
    request: Request,
    payload: Optional[models.CardStatusUpdateRequest] = Body(default=None)
):
    card = payload.CardNumber if payload else None
    new_status = payload.NewCardStatus if payload else "BLOCKED"
    return await process_mock_response(
        request,
        endpoint_key="card_status_update",
        root_tag="StatusResponse",
        random_generator=gen.generate_random_card_update,
        gen_kwargs={"req_card": card, "new_status": new_status}
    )


# --- 8. Cheque Issued Summary ---
@router.post(
    "/cheques/issued/summary",
    summary="Cheque Issued Summary",
    response_model=models.ChequeIssuedSummaryResponse
)
async def cheque_issued_summary(
    request: Request,
    payload: Optional[models.ChequeIssuedSummaryRequest] = Body(default=None)
):
    cif = payload.CustomerId if payload else None
    return await process_mock_response(
        request,
        endpoint_key="cheque_issued_summary",
        root_tag="ChequeIssuedSummaryResponse",
        random_generator=gen.generate_random_cheque_issued_summary,
        gen_kwargs={"cif": cif}
    )


# --- 9. Cheque Issued Detail ---
@router.post(
    "/cheques/issued/details",
    summary="Cheque Issued Detail",
    response_model=models.ChequeIssuedDetailResponse
)
async def cheque_issued_details(
    request: Request,
    payload: Optional[models.ChequeIssuedDetailRequest] = Body(default=None)
):
    cif = payload.CustomerId if payload else None
    return await process_mock_response(
        request,
        endpoint_key="cheque_issued_details",
        root_tag="ChequeIssuedDetailResponse",
        random_generator=gen.generate_random_cheque_issued_details,
        gen_kwargs={"cif": cif}
    )


# --- 10. Cheque Deposited Summary ---
@router.post(
    "/cheques/deposited/summary",
    summary="Cheque Deposited Summary",
    response_model=models.ChequeDepositedSummaryResponse
)
async def cheque_deposited_summary(
    request: Request,
    payload: Optional[models.ChequeDepositedSummaryRequest] = Body(default=None)
):
    cif = payload.CustomerId if payload else None
    return await process_mock_response(
        request,
        endpoint_key="cheque_deposited_summary",
        root_tag="ChequeDepositedSummaryResponse",
        random_generator=gen.generate_random_cheque_deposited_summary,
        gen_kwargs={"cif": cif}
    )


# --- 11. Cheque Deposited Detail ---
@router.post(
    "/cheques/deposited/details",
    summary="Cheque Deposited Detail",
    response_model=models.ChequeDepositedDetailResponse
)
async def cheque_deposited_details(
    request: Request,
    payload: Optional[models.ChequeDepositedDetailRequest] = Body(default=None)
):
    cif = payload.CustomerId if payload else None
    return await process_mock_response(
        request,
        endpoint_key="cheque_deposited_details",
        root_tag="ChequeDepositedDetailResponse",
        random_generator=gen.generate_random_cheque_deposited_details,
        gen_kwargs={"cif": cif}
    )


# --- 12. Passed and Stopped Cheque Inquiry ---
@router.post(
    "/cheques/status/inquiry",
    summary="Passed and Stopped Cheque Inquiry",
    response_model=models.ChequeStatusResponse
)
async def cheque_status_inquiry(
    request: Request,
    payload: Optional[models.ChequeStatusRequest] = Body(default=None)
):
    acc = payload.AccountId if payload else None
    chq = payload.ChequeNumber if payload else None
    return await process_mock_response(
        request,
        endpoint_key="cheque_status_inquiry",
        root_tag="ChequeStatusResponse",
        random_generator=gen.generate_random_cheque_status,
        gen_kwargs={"acc": acc, "chq": chq}
    )


# --- 13. Interest Certificate ---
@router.post(
    "/certificates/interest",
    summary="Interest Certificate",
    response_model=models.InterestCertificateResponse
)
async def interest_certificate(
    request: Request,
    payload: Optional[models.InterestCertificateRequest] = Body(default=None)
):
    cif = payload.CustomerId if payload else None
    year = payload.FinancialYear if payload else "2026"
    return await process_mock_response(
        request,
        endpoint_key="interest_certificate",
        root_tag="InterestCertificateResponse",
        random_generator=gen.generate_random_interest_cert,
        gen_kwargs={"cif": cif, "year": year}
    )


# --- 14. TDS Certificate ---
@router.post(
    "/certificates/tds",
    summary="TDS Certificate",
    response_model=models.TDSCertificateResponse
)
async def tds_certificate(
    request: Request,
    payload: Optional[models.TDSCertificateRequest] = Body(default=None)
):
    cif = payload.CustomerId if payload else None
    year = payload.FinancialYear if payload else "2026"
    return await process_mock_response(
        request,
        endpoint_key="tds_certificate",
        root_tag="TDSCertificateResponse",
        random_generator=gen.generate_random_tds_cert,
        gen_kwargs={"cif": cif, "year": year}
    )


# --- 15. Locker Inquiry ---
@router.post(
    "/lockers/inquiry",
    summary="Locker Inquiry",
    response_model=models.LockerInquiryResponse
)
async def locker_inquiry(
    request: Request,
    payload: Optional[models.LockerInquiryRequest] = Body(default=None)
):
    branch = payload.BranchCode if payload else "001"
    return await process_mock_response(
        request,
        endpoint_key="locker_inquiry",
        root_tag="LockerInquiryResponse",
        random_generator=gen.generate_random_locker_inquiry,
        gen_kwargs={"branch": branch}
    )


# --- 16. Mobile Validation ---
@router.post(
    "/customers/mobile/validate",
    summary="Mobile Validation",
    response_model=models.MobileValidationResponse
)
async def mobile_validation(
    request: Request,
    payload: Optional[models.MobileValidationRequest] = Body(default=None)
):
    cif = payload.CustomerId if payload else None
    mobile = payload.MobileNumber if payload else None
    return await process_mock_response(
        request,
        endpoint_key="mobile_validation",
        root_tag="MobileValidationResponse",
        random_generator=gen.generate_random_mobile_validation,
        gen_kwargs={"cif": cif, "mobile": mobile}
    )


# --- 17. Term Deposit Trial Closure ---
@router.post(
    "/deposits/td/trial-closure",
    summary="Term Deposit Trial Closure",
    response_model=models.TDTrialClosureResponse
)
async def td_trial_closure(
    request: Request,
    payload: Optional[models.TDTrialClosureRequest] = Body(default=None)
):
    acc = payload.TDAccountId if payload else None
    return await process_mock_response(
        request,
        endpoint_key="td_trial_closure",
        root_tag="TDTrialClosureResponse",
        random_generator=gen.generate_random_td_trial_closure,
        gen_kwargs={"acc": acc}
    )


# --- 18. Upcoming Payments ---
@router.post(
    "/payments/upcoming",
    summary="Upcoming Payments",
    response_model=models.UpcomingPaymentsResponse
)
async def upcoming_payments(
    request: Request,
    payload: Optional[models.UpcomingPaymentsRequest] = Body(default=None)
):
    cif = payload.CustomerId if payload else None
    return await process_mock_response(
        request,
        endpoint_key="upcoming_payments",
        root_tag="UpcomingPaymentsResponse",
        random_generator=gen.generate_random_upcoming_payments,
        gen_kwargs={"cif": cif}
    )


# --- 19. Upcoming Income ---
@router.post(
    "/income/upcoming",
    summary="Upcoming Income",
    response_model=models.UpcomingIncomeResponse
)
async def upcoming_income(
    request: Request,
    payload: Optional[models.UpcomingIncomeRequest] = Body(default=None)
):
    cif = payload.CustomerId if payload else None
    return await process_mock_response(
        request,
        endpoint_key="upcoming_income",
        root_tag="UpcomingIncomeResponse",
        random_generator=gen.generate_random_upcoming_income,
        gen_kwargs={"cif": cif}
    )


# --- 20. Cheque Leaves Status ---
@router.post(
    "/cheques/leaves/status",
    summary="Cheque Leaves Status",
    response_model=models.ChequeLeavesStatusResponse
)
async def cheque_leaves_status(
    request: Request,
    payload: Optional[models.ChequeLeavesStatusRequest] = Body(default=None)
):
    acc = payload.AccountId if payload else None
    return await process_mock_response(
        request,
        endpoint_key="cheque_leaves_status",
        root_tag="ChequeLeavesStatusResponse",
        random_generator=gen.generate_random_cheque_leaves_status,
        gen_kwargs={"acc": acc}
    )


# --- Mock Configuration Management Endpoints ---
@router.get("/mock-config", tags=["Mock Configuration Management"])
async def get_mock_config():
    """Retrieve current mock server JSON configuration."""
    return config_manager.config


@router.put("/mock-config/{endpoint_key}", tags=["Mock Configuration Management"])
async def update_endpoint_config(endpoint_key: str, new_config: Dict[str, Any] = Body(...)):
    """Update mock configuration for a specific endpoint (mode: static|random|error, delay_ms, data, etc.)."""
    config_manager.update_endpoint_config(endpoint_key, new_config)
    return {"status": "success", "message": f"Updated configuration for {endpoint_key}", "config": new_config}


@router.post("/mock-config/reload", tags=["Mock Configuration Management"])
async def reload_mock_config():
    """Reload mock configuration from mock_config.json file."""
    config_manager.load_config()
    return {"status": "success", "message": "Reloaded mock_config.json"}

from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
from digital_backend.schemas.common import ApiResponse, BaseApiResponse
from digital_backend.schemas.admin_schemas import (
    AdminCustomerSummary,
    AdminCustomer360Detail,
    AdminCustomerOnboardRequest,
    AdminCifLinkageRequest,
    AdminCustomerStatusUpdateRequest
)
from digital_backend.mock_store import mock_db

router = APIRouter(prefix="/customers", tags=["2. Admin Customer & CIF Operations (US-21, US-02)"])

@router.get("", response_model=ApiResponse[List[AdminCustomerSummary]], summary="Search & List Customer Records")
async def list_customers(
    search: Optional[str] = Query(default=None, description="Search by CIF, Name, PAN, or Mobile"),
    segment: Optional[str] = Query(default=None, description="RETAIL, CORPORATE, NRI")
):
    """
    Search customer repository across CIFs, names, segments, and KYC statuses.
    """
    summaries = []
    for c in mock_db.customers.values():
        if segment and c["customer_type"] != segment:
            continue
        if search:
            s = search.lower()
            if not (s in c["cif"].lower() or s in c["name"].lower() or s in c["mobile_number"]):
                continue
        summaries.append(AdminCustomerSummary(
            cif=c["cif"],
            customer_name=c["name"],
            customer_type=c["customer_type"],
            mobile_number=c["mobile_number"],
            email=c["email"],
            pan_number=c["pan_number"],
            kyc_status=c["kyc_status"],
            digital_profile_status=c["digital_profile_status"],
            total_accounts=len([a for a in mock_db.accounts.values() if a["cif"] == c["cif"]]),
            total_balance=sum([a["available_balance"] for a in mock_db.accounts.values() if a["cif"] == c["cif"]]),
            created_at="2024-01-15"
        ))
    return ApiResponse(data=summaries, message="Customer search completed")


@router.get("/{cif}", response_model=ApiResponse[AdminCustomer360Detail], summary="Get Customer 360 Single-Pane View")
async def get_customer_360(cif: str):
    """
    Returns unified 360-degree banking view of customer: CIF, demographics, KYC, accounts, cards, loans, deposits.
    """
    cust = mock_db.customers.get(cif)
    if not cust:
        raise HTTPException(status_code=404, detail=f"Customer with CIF {cif} not found")

    linked_accs = [a for a in mock_db.accounts.values() if a["cif"] == cif]
    linked_cards = [c for c in mock_db.cards if c["cif"] == cif]
    linked_loans = [ln for ln in mock_db.loans if ln["cif"] == cif]
    linked_deposits = [d for d in mock_db.deposits if d["cif"] == cif]

    detail = AdminCustomer360Detail(
        cif=cust["cif"],
        customer_name=cust["name"],
        customer_type=cust["customer_type"],
        dob_or_incorporation=cust.get("dob_or_incorporation", "1992-05-14"),
        gender=cust.get("gender", "MALE"),
        mobile_number=cust["mobile_number"],
        email=cust["email"],
        pan_number=cust["pan_number"],
        aadhaar_masked=cust.get("aadhaar_masked", "XXXX-XXXX-9182"),
        address=cust.get("address", "102, Palm Heights, Bandra West, Mumbai"),
        kyc_status=cust["kyc_status"],
        kyc_verified_on=cust.get("kyc_verified_on", "2024-01-16"),
        digital_profile_linked=cust["digital_profile_status"] == "ACTIVE",
        digital_status=cust["digital_profile_status"],
        risk_rating=cust.get("risk_rating", "LOW"),
        home_branch=cust.get("home_branch", "Nariman Point (001)"),
        accounts=linked_accs,
        cards=linked_cards,
        loans=linked_loans,
        deposits=linked_deposits
    )
    return ApiResponse(data=detail, message="Customer 360 retrieved successfully")


@router.post("/onboard", response_model=ApiResponse[dict], summary="Admin Branch-Assisted Onboarding (US-02)")
async def admin_onboard_customer(payload: AdminCustomerOnboardRequest):
    """
    Branch assisted digital onboarding for customers who cannot self-register (PRD US-02).
    """
    mock_db.customers[payload.cif] = {
        "cif": payload.cif,
        "name": payload.customer_name,
        "customer_type": payload.customer_type,
        "mobile_number": payload.mobile_number,
        "email": payload.email,
        "pan_number": payload.pan_number,
        "kyc_status": "VERIFIED",
        "digital_profile_status": "ACTIVE",
        "risk_rating": "LOW",
        "home_branch": payload.branch_code,
        "last_login": "Never"
    }

    # Log action for audit
    mock_db.audit_logs.insert(0, {
        "log_id": f"AUDIT-ONBOARD-{payload.cif}",
        "timestamp": "2026-09-07T06:30:00Z",
        "admin_user": "rajesh.amin",
        "action_type": "BRANCH_CUSTOMER_ONBOARD",
        "target_resource_id": payload.cif,
        "ip_address": "10.20.4.115",
        "status": "SUCCESS"
    })

    return ApiResponse(
        data={"cif": payload.cif, "status": "ONBOARDED", "activation_sms_sent": True},
        message=f"Customer {payload.customer_name} onboarded successfully. Temporary credentials sent to {payload.mobile_number}."
    )


@router.post("/cif-linkage", response_model=BaseApiResponse, summary="Link / Unlink CIF to Digital Banking Profile (US-21)")
async def manage_cif_linkage(payload: AdminCifLinkageRequest):
    """
    Links core banking CIF to digital banking app identity (PRD US-21).
    """
    cust = mock_db.customers.get(payload.cif)
    if not cust:
        raise HTTPException(status_code=404, detail="CIF not found in Core Banking System")

    cust["digital_profile_status"] = "ACTIVE" if payload.action == "LINK" else "UNLINKED"
    return BaseApiResponse(
        success=True,
        response_code="BB-200",
        message=f"CIF {payload.cif} has been successfully {payload.action.lower()}ed to digital profile {payload.mobile_user_id}."
    )


@router.put("/{cif}/status", response_model=BaseApiResponse, summary="Update Digital Profile Status (Freeze / Block)")
async def update_customer_status(cif: str, payload: AdminCustomerStatusUpdateRequest):
    """
    Update customer status (ACTIVE, BLOCKED, FROZEN).
    """
    cust = mock_db.customers.get(cif)
    if not cust:
        raise HTTPException(status_code=404, detail="CIF not found")

    cust["digital_profile_status"] = payload.new_status
    return BaseApiResponse(
        success=True,
        response_code="BB-200",
        message=f"Customer {cif} status updated to {payload.new_status}. Reason: {payload.reason}"
    )

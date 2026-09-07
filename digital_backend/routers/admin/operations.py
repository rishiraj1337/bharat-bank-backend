from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
from digital_backend.schemas.common import ApiResponse, BaseApiResponse
from digital_backend.schemas.admin_schemas import (
    AdminTransactionMonitorItem,
    StatusOverrideRequest,
    ServiceRequestItem,
    ServiceRequestActionRequest
)
from digital_backend.schemas.flutter_schemas import SubsystemHealth
from digital_backend.mock_store import mock_db

router = APIRouter(prefix="/operations", tags=["4. Admin Real-Time Operations & Monitoring"])

@router.get("/transactions", response_model=ApiResponse[List[AdminTransactionMonitorItem]], summary="Live Transaction Ledger Stream")
async def monitor_transactions(
    status: Optional[str] = Query(default=None, description="SUCCESS, PENDING, FAILED"),
    payment_mode: Optional[str] = Query(default=None, description="IMPS, NEFT, RTGS, BBPS")
):
    """
    Real-time monitoring stream of all switch transactions across channels.
    """
    items = [
        AdminTransactionMonitorItem(
            txn_id="TXN-20260907-88912",
            utr="UTR-IMPS-20260907-99120",
            channel="MOBILE_APP",
            payment_mode="IMPS",
            sender_cif="CIF100001",
            sender_name="Arjun Mehta",
            sender_account="101000000012",
            receiver_name="Sneha Mehta",
            receiver_account="99182390129182",
            receiver_bank="Bharat Co-operative Bank",
            amount=5000.00,
            status="SUCCESS",
            created_at="2026-09-07T06:15:00Z",
            switch_response_code="00",
            risk_score=12
        ),
        AdminTransactionMonitorItem(
            txn_id="TXN-20260907-88911",
            utr="UTR-NEFT-20260907-77219",
            channel="ADMIN_PORTAL",
            payment_mode="NEFT",
            sender_cif="CIF-CORP-9001",
            sender_name="Nexus Tech Enterprises",
            sender_account="101000009943",
            receiver_name="Amazon Web Services",
            receiver_account="02938102938182",
            receiver_bank="Citibank",
            amount=250000.00,
            status="SUCCESS",
            created_at="2026-09-07T06:00:00Z",
            switch_response_code="00",
            risk_score=5
        )
    ]
    return ApiResponse(data=items, message="Transaction monitor stream fetched")


@router.post("/transactions/{txn_id}/status-override", response_model=BaseApiResponse, summary="Manual Reconciliation Status Override")
async def override_transaction_status(txn_id: str, payload: StatusOverrideRequest):
    """
    Manual ops intervention to mark timeout/pending transaction as settled or failed with audit trail.
    """
    mock_db.audit_logs.insert(0, {
        "log_id": f"AUDIT-TXN-OVERRIDE-{txn_id}",
        "timestamp": "2026-09-07T06:30:00Z",
        "admin_user": "rajesh.amin",
        "action_type": "TXN_STATUS_OVERRIDE",
        "target_resource_id": txn_id,
        "ip_address": "10.20.4.115",
        "new_value": {"override_status": payload.new_status, "reason": payload.reason},
        "status": "SUCCESS"
    })
    return BaseApiResponse(
        success=True,
        response_code="BB-200",
        message=f"Transaction {txn_id} overridden to {payload.new_status}."
    )


@router.get("/service-requests", response_model=ApiResponse[List[ServiceRequestItem]], summary="List Customer Service Requests")
async def list_service_requests():
    """
    Lists customer requests (Cheque book, address update, card replacement, disputes) awaiting branch action.
    """
    items = [ServiceRequestItem(**sr) for sr in mock_db.service_requests]
    return ApiResponse(data=items, message="Service requests fetched")


@router.put("/service-requests/{req_id}/action", response_model=BaseApiResponse, summary="Action Service Request (Approve / Reject / Dispatch)")
async def action_service_request(req_id: str, payload: ServiceRequestActionRequest):
    """
    Approve, reject or fulfill customer service request.
    """
    for sr in mock_db.service_requests:
        if sr["request_id"] == req_id:
            sr["status"] = payload.action
            return BaseApiResponse(success=True, response_code="BB-200", message=f"Service request {req_id} updated to {payload.action}.")
    raise HTTPException(status_code=404, detail="Service request not found")


@router.get("/system-health", response_model=ApiResponse[List[SubsystemHealth]], summary="Live Infrastructure & Microservices Health")
async def get_system_health():
    """
    Health dashboard monitoring all upstream and downstream banking integrations.
    """
    subsystems = [
        SubsystemHealth(name="CBS Core Banking (Oracle FLEXCUBE)", status="UP", latency_ms=14.2),
        SubsystemHealth(name="NPST Unified Payment Switch", status="UP", latency_ms=8.5),
        SubsystemHealth(name="NPCI BBPS Central Unit", status="UP", latency_ms=22.1),
        SubsystemHealth(name="SMS Gateway (Karix / Gupshup)", status="UP", latency_ms=5.0),
        SubsystemHealth(name="UIDAI Aadhaar Verification Service", status="UP", latency_ms=45.3),
        SubsystemHealth(name="NSDL PAN Verification API", status="UP", latency_ms=32.0)
    ]
    return ApiResponse(data=subsystems, message="System health status OK")

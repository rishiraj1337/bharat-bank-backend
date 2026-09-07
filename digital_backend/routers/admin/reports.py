from fastapi import APIRouter, Query
from typing import List, Optional
import uuid
from digital_backend.schemas.common import ApiResponse
from digital_backend.schemas.admin_schemas import (
    AuditLogRecord,
    ReportExportRequest,
    ReportExportResponse
)
from digital_backend.mock_store import mock_db

router = APIRouter(prefix="/reports", tags=["5. Admin Reports & Audit Trail (US-23)"])

@router.get("/audit-logs", response_model=ApiResponse[List[AuditLogRecord]], summary="Audit Log Trail Explorer")
async def get_audit_logs(
    admin_user: Optional[str] = Query(default=None, description="Filter by acting administrator")
):
    """
    Search immutable audit trail of all staff and system modifications (PRD US-23).
    """
    items = [AuditLogRecord(**al) for al in mock_db.audit_logs]
    if admin_user:
        items = [al for al in items if al.admin_user == admin_user]
    return ApiResponse(data=items, message="Audit trail logs retrieved")


@router.get("/customer-summary", response_model=ApiResponse[dict], summary="Customer Analytics & Acquisition Summary")
async def get_customer_summary_report():
    """
    High-level operational metrics on retail and corporate customer volume.
    """
    return ApiResponse(
        data={
            "total_registered_customers": 14250,
            "active_digital_users_30d": 11890,
            "retail_accounts_count": 22400,
            "corporate_accounts_count": 1850,
            "total_deposits_aum": 845000000.00,
            "total_loans_book": 412000000.00,
            "as_of_timestamp": "2026-09-07T06:30:00Z"
        },
        message="Customer analytics report generated"
    )


@router.post("/export", response_model=ApiResponse[ReportExportResponse], summary="Generate Report Export (CSV / Excel / PDF)")
async def export_report(payload: ReportExportRequest):
    """
    Asynchronously builds and returns download URI for regulatory and operational reports (PRD US-23).
    """
    exp_id = f"EXP-{uuid.uuid4().hex[:6].upper()}"
    file_ext = payload.format.lower()
    res = ReportExportResponse(
        export_id=exp_id,
        report_name=f"BharatBank_{payload.report_type}_{payload.from_date}_{payload.to_date}.{file_ext}",
        download_url=f"https://reports.bharatbank.com/exports/{exp_id}.{file_ext}",
        generated_at="2026-09-07T06:30:00Z",
        record_count=1450,
        file_size_kb=480.5
    )
    return ApiResponse(data=res, message=f"{payload.report_type} report exported successfully in {payload.format} format")

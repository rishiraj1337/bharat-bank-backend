from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
from digital_backend.schemas.common import ApiResponse, BaseApiResponse
from digital_backend.schemas.admin_schemas import (
    RPMApplicationSummary,
    LoanDocumentItem,
    LoanUnderwritingDecisionRequest,
    LoanDisbursementRequest
)
from digital_backend.mock_store import mock_db

router = APIRouter(prefix="/loans-underwriting", tags=["8. Admin Loan Underwriting & RPM Origination (OBDX / CBS v3)"])

@router.get("/applications", response_model=ApiResponse[List[RPMApplicationSummary]], summary="List Loan Applications (OBDX / RPM Process Driver)")
async def list_loan_applications(
    status: Optional[str] = Query(default=None, description="UNDER_REVIEW, SANCTIONED, DISBURSED"),
    product_sub_type: Optional[str] = Query(default=None, description="HOME_LOAN, AUTO_LOAN, PERSONAL_LOAN")
):
    """
    Direct integration with Oracle OBDX/RPM v3 Process Driver & Applications List:
    Inquires loan origination applications submitted via mobile or branch.
    """
    apps = [RPMApplicationSummary(**a) for a in getattr(mock_db, "loan_applications", [])]
    if status:
        apps = [a for a in apps if a.status == status]
    if product_sub_type:
        apps = [a for a in apps if a.product_sub_type == product_sub_type]
    return ApiResponse(data=apps, message="Loan applications retrieved from RPM origination engine")


@router.get("/applications/{app_no}", response_model=ApiResponse[dict], summary="Get Detailed Application & Domain Data")
async def get_application_detail(app_no: str):
    """
    Fetches full domain data (Applicant profile, credit score, requested amount, tenure, income proofs) matching CBS v3 `process_get_data`.
    """
    for a in mock_db.loan_applications:
        if a["application_no"] == app_no:
            return ApiResponse(
                data={
                    "application_summary": RPMApplicationSummary(**a),
                    "domain_applicant_data": {
                        "first_name": a["customer_name"].split()[0],
                        "last_name": a["customer_name"].split()[-1] if len(a["customer_name"].split()) > 1 else "",
                        "mobile": a["mobile_number"],
                        "cif": a["cif"],
                        "cibil_score": a["risk_score"],
                        "monthly_income": 180000.00,
                        "existing_obligations": 25000.00,
                        "foir_percentage": 37.5
                    },
                    "checklist_documents": a.get("documents", [])
                },
                message="Application 360 data retrieved"
            )
    raise HTTPException(status_code=404, detail="Application not found")


@router.get("/applications/{app_no}/documents", response_model=ApiResponse[List[LoanDocumentItem]], summary="Get Checklist Documents (CBS v3 process_get_document_list)")
async def get_application_documents(app_no: str):
    """
    Retrieves required and uploaded documents for underwriting verification.
    """
    for a in mock_db.loan_applications:
        if a["application_no"] == app_no:
            docs = [LoanDocumentItem(**d) for d in a.get("documents", [])]
            return ApiResponse(data=docs, message="Documents retrieved")
    raise HTTPException(status_code=404, detail="Application not found")


@router.put("/applications/{app_no}/documents/{doc_id}/verify", response_model=BaseApiResponse, summary="Verify Underwriting Document")
async def verify_document(app_no: str, doc_id: str, status: str = "VERIFIED"):
    """
    Underwriter marks KYC, income proof or collateral document as VERIFIED or REJECTED.
    """
    for a in mock_db.loan_applications:
        if a["application_no"] == app_no:
            for d in a.get("documents", []):
                if d["document_id"] == doc_id:
                    d["status"] = status
                    d["verified_by"] = "priya.sharma"
                    return BaseApiResponse(success=True, response_code="BB-200", message=f"Document {doc_id} marked as {status}.")
    raise HTTPException(status_code=404, detail="Document not found")


@router.post("/applications/{app_no}/decision", response_model=ApiResponse[dict], summary="Underwriting Decision (Sanction / Reject)")
async def underwrite_decision(app_no: str, payload: LoanUnderwritingDecisionRequest):
    """
    Underwriter issues final sanction letter or rejection with reason code.
    """
    for a in mock_db.loan_applications:
        if a["application_no"] == app_no:
            a["status"] = "SANCTIONED" if payload.decision == "APPROVE" else "REJECTED"
            return ApiResponse(
                data={
                    "application_no": app_no,
                    "decision": payload.decision,
                    "sanctioned_amount": payload.sanctioned_amount,
                    "sanctioned_interest_rate": payload.sanctioned_interest_rate,
                    "sanction_letter_url": f"https://docs.bharatbank.com/sanctions/{app_no}.pdf",
                    "remarks": payload.remarks
                },
                message=f"Application {app_no} {payload.decision} completed successfully."
            )
    raise HTTPException(status_code=404, detail="Application not found")


@router.post("/applications/{app_no}/disburse", response_model=ApiResponse[dict], summary="Trigger Core CBS Loan Disbursement")
async def disburse_loan(app_no: str, payload: LoanDisbursementRequest):
    """
    Credits sanctioned loan funds into customer account and generates repayment schedule in CBS.
    """
    acc = mock_db.accounts.get(payload.disbursement_account_number)
    if not acc:
        raise HTTPException(status_code=404, detail="Disbursement account not found in CBS")

    acc["available_balance"] += payload.amount
    acc["ledger_balance"] += payload.amount

    for a in mock_db.loan_applications:
        if a["application_no"] == app_no:
            a["status"] = "DISBURSED"

    return ApiResponse(
        data={
            "application_no": app_no,
            "disbursed_to_account": payload.disbursement_account_number,
            "amount_disbursed": payload.amount,
            "cbs_loan_account_number": f"LN{app_no.replace('APP', '')}",
            "disbursement_utr": "UTR-DISB-20260907-88912",
            "new_account_balance": acc["available_balance"]
        },
        message="Loan successfully disbursed in CBS"
    )

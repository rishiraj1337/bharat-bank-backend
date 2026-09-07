from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
import uuid
from datetime import datetime
from digital_backend.schemas.common import ApiResponse, BaseApiResponse
from digital_backend.schemas.flutter_schemas import (
    TransferTypeOption,
    TransferInitiateRequest,
    TransferInitiateResponse,
    ScheduleTransferRequest,
    IfscLookupResponse
)
from digital_backend.mock_store import mock_db

router = APIRouter(prefix="/transfers", tags=["5. App Fund Transfers"])

@router.get("/transfer-types", response_model=ApiResponse[List[TransferTypeOption]], summary="Get Fund Transfer Rails (UI Options)")
async def get_transfer_types():
    """
    Returns transfer options matching the mobile app selection screen:
    - Within Bank: Transfer between your Bharat Bank accounts
    - IMPS: Instant transfer 24x7 · up to ₹5 lakh
    - NEFT: Batch settlement during banking hours
    - RTGS: High-value same-day · ₹2 lakh and above
    """
    options = [
        TransferTypeOption(
            code="WITHIN_BANK",
            title="Within Bank",
            subtitle="Transfer between your Bharat Bank accounts",
            icon="swap_horiz",
            min_amount=1.0,
            max_amount=5000000.0,
            charge=0.0,
            settlement_type="Instant (24x7)"
        ),
        TransferTypeOption(
            code="IMPS",
            title="IMPS",
            subtitle="Instant transfer 24x7 · up to ₹5 lakh",
            icon="bolt",
            min_amount=1.0,
            max_amount=500000.0,
            charge=0.0,
            settlement_type="Instant (24x7)"
        ),
        TransferTypeOption(
            code="NEFT",
            title="NEFT",
            subtitle="Batch settlement during banking hours",
            icon="schedule",
            min_amount=1.0,
            max_amount=2500000.0,
            charge=0.0,
            settlement_type="Hourly Batches"
        ),
        TransferTypeOption(
            code="RTGS",
            title="RTGS",
            subtitle="High-value same-day · ₹2 lakh and above",
            icon="account_balance",
            min_amount=200000.0,
            max_amount=10000000.0,
            charge=0.0,
            settlement_type="Real Time"
        )
    ]
    return ApiResponse(data=options, message="Transfer types fetched")


@router.post("/initiate", response_model=ApiResponse[TransferInitiateResponse], summary="Initiate Fund Transfer (Screen 4 Match)")
async def initiate_fund_transfer(payload: TransferInitiateRequest):
    """
    Unified Fund Transfer Initiation matching Screenshot 4:
    - Deducts amount from chosen debit account
    - Validates beneficiary and limits
    - Returns UTR, transaction reference, and updated remaining balance.
    """
    debit_acc = mock_db.accounts.get(payload.debit_account_number)
    if not debit_acc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "ACCOUNT_NOT_FOUND", "message": f"Account {payload.debit_account_number} not found"}
        )

    if debit_acc["available_balance"] < payload.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INSUFFICIENT_FUNDS", "message": f"Insufficient balance in account {payload.debit_account_number}"}
        )

    if payload.transfer_type == "RTGS" and payload.amount < 200000.0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "MIN_RTGS_LIMIT", "message": "Minimum amount for RTGS transfer is ₹2,00,000"}
        )

    # Update balance in mock store
    debit_acc["available_balance"] -= payload.amount
    remaining_balance = debit_acc["available_balance"]

    txn_id = f"TXN-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
    utr_code = f"UTR-{payload.transfer_type}-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

    # Record transaction
    mock_db.transactions.insert(0, {
        "transaction_id": txn_id,
        "reference_no": utr_code,
        "account_number": payload.debit_account_number,
        "cif": debit_acc["cif"],
        "title": payload.beneficiary_name,
        "subtitle": f"Today, {datetime.now().strftime('%I:%M %p')} • {payload.transfer_type}",
        "date_formatted": f"Today, {datetime.now().strftime('%I:%M %p')}",
        "transaction_date": datetime.utcnow().strftime("%Y-%m-%d"),
        "value_date": datetime.utcnow().strftime("%Y-%m-%d"),
        "narration": f"{payload.transfer_type}/{payload.beneficiary_name}/{payload.note or 'Transfer'}",
        "payment_mode": payload.transfer_type,
        "channel": "MOBILE",
        "amount": payload.amount,
        "formatted_amount": f"-₹{payload.amount:,.2f}",
        "type": "DEBIT",
        "status": "Success",
        "category": "Transfer",
        "balance_after": remaining_balance,
        "icon": "arrow_outward"
    })

    response = TransferInitiateResponse(
        transaction_id=txn_id,
        utr=utr_code,
        reference_no=f"REF-{uuid.uuid4().hex[:8].upper()}",
        status="SUCCESS",
        amount=payload.amount,
        formatted_amount=f"₹{payload.amount:,.2f}",
        fee=0.00,
        debit_account_number=payload.debit_account_number,
        receiver_name=payload.beneficiary_name,
        receiver_bank=payload.beneficiary_bank_name or "Bharat Co-operative Bank",
        receiver_masked_account=f"**** **** {payload.beneficiary_account_number[-4:]}",
        transfer_type=payload.transfer_type,
        note=payload.note,
        timestamp=datetime.utcnow().isoformat() + "Z",
        balance_remaining=remaining_balance
    )

    return ApiResponse(data=response, message="Transfer processed successfully")


@router.post("/within-bank", response_model=ApiResponse[TransferInitiateResponse], summary="Direct Within-Bank Transfer")
async def transfer_within_bank(payload: TransferInitiateRequest):
    """
    Intrabank transfer between Bharat Bank accounts.
    """
    payload.transfer_type = "WITHIN_BANK"
    return await initiate_fund_transfer(payload)


@router.post("/imps", response_model=ApiResponse[TransferInitiateResponse], summary="IMPS Fund Transfer (Instant 24x7)")
async def transfer_imps(payload: TransferInitiateRequest):
    """
    IMPS fund transfer through NPST switch.
    """
    payload.transfer_type = "IMPS"
    return await initiate_fund_transfer(payload)


@router.post("/neft", response_model=ApiResponse[TransferInitiateResponse], summary="NEFT Fund Transfer")
async def transfer_neft(payload: TransferInitiateRequest):
    """
    NEFT batch transfer.
    """
    payload.transfer_type = "NEFT"
    return await initiate_fund_transfer(payload)


@router.post("/rtgs", response_model=ApiResponse[TransferInitiateResponse], summary="RTGS Fund Transfer (High Value)")
async def transfer_rtgs(payload: TransferInitiateRequest):
    """
    RTGS transfer for amounts >= ₹2,00,000.
    """
    payload.transfer_type = "RTGS"
    return await initiate_fund_transfer(payload)


@router.post("/quick-transfer", response_model=ApiResponse[TransferInitiateResponse], summary="Quick Transfer Without Saving Payee")
async def quick_transfer(payload: TransferInitiateRequest):
    """
    Ad-hoc instant transfer without prior beneficiary cooling period (max ₹25,000).
    """
    if payload.amount > 25000.0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "QUICK_TRANSFER_LIMIT_EXCEEDED", "message": "Quick transfer limit is ₹25,000. Please add payee for higher amounts."}
        )
    return await initiate_fund_transfer(payload)


@router.post("/schedule", response_model=ApiResponse[dict], summary="Schedule One-Time or Recurring Transfer")
async def schedule_transfer(payload: ScheduleTransferRequest):
    """
    Set up scheduled transfer or recurring standing instruction.
    """
    sch_id = f"SCH-{uuid.uuid4().hex[:6].upper()}"
    new_schedule = {
        "schedule_id": sch_id,
        "cif": "CIF100001",
        "debit_account_number": payload.debit_account_number,
        "beneficiary_name": payload.beneficiary_name,
        "beneficiary_account_number": payload.beneficiary_account_number,
        "beneficiary_ifsc": payload.beneficiary_ifsc,
        "amount": payload.amount,
        "frequency": payload.frequency,
        "next_execution_date": payload.start_date,
        "transfer_type": payload.transfer_type,
        "status": "ACTIVE"
    }
    mock_db.scheduled_transfers.append(new_schedule)
    return ApiResponse(data=new_schedule, message="Scheduled transfer created successfully")


@router.get("/scheduled", response_model=ApiResponse[List[dict]], summary="List Active Scheduled Transfers")
async def list_scheduled_transfers():
    """
    Returns list of recurring and upcoming scheduled transfers.
    """
    return ApiResponse(data=mock_db.scheduled_transfers, message="Scheduled transfers list")


@router.delete("/scheduled/{schedule_id}", response_model=BaseApiResponse, summary="Cancel Scheduled Transfer")
async def cancel_scheduled_transfer(schedule_id: str):
    """
    Cancel an active standing instruction or scheduled payment.
    """
    mock_db.scheduled_transfers = [s for s in mock_db.scheduled_transfers if s["schedule_id"] != schedule_id]
    return BaseApiResponse(success=True, response_code="BB-200", message="Scheduled transfer cancelled successfully")


@router.get("/lookup-ifsc/{ifsc_code}", response_model=ApiResponse[IfscLookupResponse], summary="Lookup Bank & Branch Details by IFSC")
async def lookup_ifsc(ifsc_code: str):
    """
    Auto-populates bank name, branch address, MICR, and supported payment rails by IFSC.
    """
    code_upper = ifsc_code.upper()
    data = IfscLookupResponse(
        ifsc=code_upper,
        bank_name="Bharat Co-operative Bank" if "BCOB" in code_upper else ("HDFC Bank" if "HDFC" in code_upper else "Bharat Bank"),
        branch_name="Main Metropolitan Branch",
        address="Ground Floor, Central Commercial Complex, Mumbai",
        city="Mumbai",
        state="Maharashtra",
        rtgs_supported=True,
        neft_supported=True,
        imps_supported=True,
        micr="400002001"
    )
    return ApiResponse(data=data, message="IFSC details found")

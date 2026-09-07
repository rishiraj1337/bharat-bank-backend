from fastapi import APIRouter, HTTPException, status
from typing import List
import uuid
from datetime import datetime

from digital_backend.schemas.common import ApiResponse, BaseApiResponse
from digital_backend.schemas.flutter_schemas import (
    BillerCategoryItem,
    BillerItem,
    FetchBillRequest,
    FetchBillResponse,
    PayBillRequest,
    ScheduleBillPaymentRequest,
    RecurringBillPaymentRequest,
    RegisteredBillerItem,
    BillPaymentStatusResponse
)
from digital_backend.mock_store import mock_db

router = APIRouter(prefix="/bills", tags=["10. App BBPS & Bill Payments (v2)"])


@router.get("/categories", response_model=ApiResponse[List[BillerCategoryItem]], summary="Get BBPS Biller Categories")
async def get_biller_categories():
    """
    Returns Bharat BillPay (BBPS) utility categories.
    """
    categories = [
        BillerCategoryItem(category_id="ELECTRICITY", category_name="Electricity", icon="flash_on"),
        BillerCategoryItem(category_id="MOBILE_POSTPAID", category_name="Mobile Postpaid", icon="phone_android"),
        BillerCategoryItem(category_id="MOBILE_PREPAID", category_name="Mobile Prepaid", icon="smartphone"),
        BillerCategoryItem(category_id="DTH", category_name="DTH / Cable TV", icon="tv"),
        BillerCategoryItem(category_id="WATER", category_name="Water Bill", icon="water_drop"),
        BillerCategoryItem(category_id="PIPED_GAS", category_name="Piped Gas", icon="local_fire_department"),
        BillerCategoryItem(category_id="BROADBAND", category_name="Broadband & Landline", icon="wifi"),
        BillerCategoryItem(category_id="FASTAG", category_name="FASTag Recharge", icon="directions_car")
    ]
    return ApiResponse(data=categories, message="Biller categories loaded")


@router.get("/billers", response_model=ApiResponse[List[BillerItem]], summary="List Billers by Category")
async def get_billers(category_id: str = "ELECTRICITY"):
    """
    Fetches live billers registered on NPCI BBPS switch for selected category.
    """
    billers = [
        BillerItem(biller_id="BLR-ADANI-MUM", biller_name="Adani Electricity Mumbai Limited", category_id="ELECTRICITY", consumer_param_name="Consumer Number (10 Digits)", sample_param_value="1029384756"),
        BillerItem(biller_id="BLR-MAHAVITARAN", biller_name="MSEDCL (Mahavitaran)", category_id="ELECTRICITY", consumer_param_name="Consumer Number (12 Digits)", sample_param_value="991823019283"),
        BillerItem(biller_id="BLR-TATA-POWER", biller_name="Tata Power - Mumbai", category_id="ELECTRICITY", consumer_param_name="Customer ID", sample_param_value="9001928301"),
        BillerItem(biller_id="BLR-AIRTEL-FIBER", biller_name="Bharti Airtel Broadband", category_id="BROADBAND", consumer_param_name="Landline / Account Number", sample_param_value="02226489102")
    ]
    filtered = [b for b in billers if b.category_id == category_id] or billers
    return ApiResponse(data=filtered, message="Billers fetched")


@router.post("/fetch-bill", response_model=ApiResponse[FetchBillResponse], summary="Fetch Real-Time Due Bill from BBPS")
async def fetch_bill(payload: FetchBillRequest):
    """
    Queries BBPS central switch to retrieve outstanding utility bill details.
    """
    response = FetchBillResponse(
        biller_id=payload.biller_id,
        biller_name="Adani Electricity Mumbai Limited",
        consumer_number=payload.consumer_number,
        customer_name="Arjun Mehta",
        bill_number="BILL-202609-88192",
        bill_date="2026-09-01",
        due_date="2026-09-20",
        bill_amount=4500.00,
        formatted_amount="₹4,500.00",
        is_bill_paid=False
    )
    return ApiResponse(data=response, message="Bill fetched successfully from BBPS switch")


@router.post("/pay", response_model=ApiResponse[dict], summary="Pay Utility Bill via BBPS")
async def pay_bill(payload: PayBillRequest):
    """
    Debits account and settles utility bill via BBPS, generating BBPS reference receipt.
    """
    debit_acc = mock_db.accounts.get(payload.debit_account_number)
    if not debit_acc or debit_acc["available_balance"] < payload.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    debit_acc["available_balance"] -= payload.amount
    bbps_ref = f"BBPS-{uuid.uuid4().hex[:8].upper()}"
    txn_id = f"BBPS-TXN-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

    # Store transaction for status inquiry
    txn_record = {
        "transaction_id": txn_id,
        "bbps_reference_no": bbps_ref,
        "biller_id": payload.biller_id,
        "biller_name": "Adani Electricity Mumbai Limited" if "ADANI" in payload.biller_id else "Utility Provider",
        "consumer_number": payload.consumer_number,
        "amount": payload.amount,
        "formatted_amount": f"₹{payload.amount:,.2f}",
        "payment_status": "SUCCESS",
        "payment_timestamp": datetime.utcnow().isoformat() + "Z",
        "payment_mode": "BBPS_DEBIT",
        "debit_account_number": payload.debit_account_number,
        "npci_txn_ref": f"NPCI{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        "receipt_url": f"https://bbps.bharatbank.com/receipts/{bbps_ref}.pdf"
    }
    mock_db.bill_transactions[txn_id] = txn_record
    mock_db.bill_transactions[bbps_ref] = txn_record

    return ApiResponse(
        data={
            "transaction_id": txn_id,
            "bbps_reference_no": bbps_ref,
            "biller_id": payload.biller_id,
            "consumer_number": payload.consumer_number,
            "amount_paid": payload.amount,
            "payment_status": "SUCCESS",
            "receipt_url": f"https://bbps.bharatbank.com/receipts/{bbps_ref}.pdf"
        },
        message="Bill paid successfully via BBPS"
    )


# --- NEW IN V2: BILL SCHEDULE ---
@router.post("/schedule", response_model=ApiResponse[dict], summary="Schedule a Future One-Time Bill Payment")
async def schedule_bill_payment(payload: ScheduleBillPaymentRequest):
    """
    Schedules a one-time utility bill payment for future automated execution prior to due date.
    """
    sch_id = f"SCH-BILL-{uuid.uuid4().hex[:6].upper()}"
    record = {
        "schedule_id": sch_id,
        "cif": "CIF100001",
        "biller_id": payload.biller_id,
        "biller_name": payload.biller_name,
        "consumer_number": payload.consumer_number,
        "debit_account_number": payload.debit_account_number,
        "amount": payload.amount,
        "formatted_amount": f"₹{payload.amount:,.2f}",
        "scheduled_date": payload.scheduled_date,
        "notes": payload.notes,
        "status": "SCHEDULED",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    mock_db.scheduled_bills.append(record)
    return ApiResponse(
        data=record,
        message=f"Bill payment of ₹{payload.amount:,.2f} scheduled successfully for {payload.scheduled_date}."
    )


# --- NEW IN V2: BILL RECURRING ---
@router.post("/recurring", response_model=ApiResponse[dict], summary="Set Up Recurring Bill Payment (Auto-Pay)")
async def setup_recurring_bill_payment(payload: RecurringBillPaymentRequest):
    """
    Sets up a recurring bill payment rule (Auto-Pay mandate) for automatic monthly settlement up to max limit.
    """
    mandate_id = f"REC-BILL-{uuid.uuid4().hex[:6].upper()}"
    record = {
        "mandate_id": mandate_id,
        "cif": "CIF100001",
        "biller_id": payload.biller_id,
        "biller_name": payload.biller_name,
        "consumer_number": payload.consumer_number,
        "debit_account_number": payload.debit_account_number,
        "max_auto_pay_amount": payload.max_auto_pay_amount,
        "formatted_max_amount": f"₹{payload.max_auto_pay_amount:,.2f}",
        "frequency": payload.frequency,
        "start_date": payload.start_date,
        "end_date": payload.end_date,
        "status": "ACTIVE",
        "next_due_date": "2026-10-01"
    }
    mock_db.recurring_bills.append(record)
    return ApiResponse(
        data=record,
        message=f"Auto-Pay mandate created successfully for {payload.biller_name} with limit up to ₹{payload.max_auto_pay_amount:,.2f}."
    )


# --- NEW IN V2: REGISTERED BILLERS ---
@router.get("/registered-billers", response_model=ApiResponse[List[RegisteredBillerItem]], summary="List Saved/Registered Billers")
async def list_registered_billers(cif: str = "CIF100001"):
    """
    Lists utility billers registered and saved under the customer's profile for quick access and auto-pay tracking.
    """
    user_billers = [b for b in mock_db.registered_billers if b.get("cif") == cif or not b.get("cif")]
    items = [RegisteredBillerItem(**b) for b in user_billers]
    return ApiResponse(data=items, message=f"Retrieved {len(items)} saved billers")


# --- NEW IN V2: DELETE REGISTERED BILLER ---
@router.delete("/registered-billers/{registered_biller_id}", response_model=BaseApiResponse, summary="Remove Saved Biller")
async def delete_registered_biller(registered_biller_id: str):
    """
    Removes a registered biller from the customer's profile.
    """
    initial_len = len(mock_db.registered_billers)
    mock_db.registered_billers = [b for b in mock_db.registered_billers if b["registered_biller_id"] != registered_biller_id]

    if len(mock_db.registered_billers) == initial_len:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "BILLER_NOT_FOUND", "message": f"Registered biller {registered_biller_id} not found"}
        )

    return BaseApiResponse(
        success=True,
        response_code="BB-200",
        message=f"Registered biller '{registered_biller_id}' removed successfully from your profile"
    )


# --- NEW IN V2: BILL PAYMENT STATUS ---
@router.get("/{transaction_id}/status", response_model=ApiResponse[BillPaymentStatusResponse], summary="Check Bill Payment Transaction Status")
async def get_bill_payment_status(transaction_id: str):
    """
    Queries final settlement and confirmation status of a BBPS utility bill payment.
    """
    txn = mock_db.bill_transactions.get(transaction_id)
    if not txn:
        # Fallback simulation if an ad-hoc transaction ID is passed
        txn = {
            "transaction_id": transaction_id,
            "bbps_reference_no": f"BBPS{uuid.uuid4().hex[:10].upper()}",
            "biller_id": "BLR-ADANI-MUM",
            "biller_name": "Adani Electricity Mumbai Limited",
            "consumer_number": "1029384756",
            "amount": 4500.00,
            "formatted_amount": "₹4,500.00",
            "payment_status": "SUCCESS",
            "payment_timestamp": datetime.utcnow().isoformat() + "Z",
            "payment_mode": "BBPS_DEBIT",
            "debit_account_number": "101000000012",
            "npci_txn_ref": f"NPCI{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "receipt_url": f"https://bbps.bharatbank.com/receipts/{transaction_id}.pdf"
        }

    return ApiResponse(
        data=BillPaymentStatusResponse(**txn),
        message=f"Transaction {transaction_id} status: {txn['payment_status']}"
    )

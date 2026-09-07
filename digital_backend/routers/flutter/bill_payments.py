from fastapi import APIRouter, HTTPException, status
from typing import List
import uuid
from digital_backend.schemas.common import ApiResponse
from digital_backend.schemas.flutter_schemas import (
    BillerCategoryItem,
    BillerItem,
    FetchBillRequest,
    FetchBillResponse,
    PayBillRequest
)
from digital_backend.mock_store import mock_db

router = APIRouter(prefix="/bills", tags=["10. App BBPS & Bill Payments"])

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
        BillerItem(biller_id="BLR-TATA-POWER", biller_name="Tata Power - Mumbai", category_id="ELECTRICITY", consumer_param_name="Customer ID", sample_param_value="9001928301")
    ]
    return ApiResponse(data=billers, message="Billers fetched")


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

    return ApiResponse(
        data={
            "bbps_reference_no": bbps_ref,
            "biller_id": payload.biller_id,
            "consumer_number": payload.consumer_number,
            "amount_paid": payload.amount,
            "payment_status": "SUCCESS",
            "receipt_url": f"https://bbps.bharatbank.com/receipts/{bbps_ref}.pdf"
        },
        message="Bill paid successfully via BBPS"
    )

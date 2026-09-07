from fastapi import APIRouter, HTTPException, status
from digital_backend.schemas.common import ApiResponse
from digital_backend.schemas.flutter_schemas import CustomerProfileResponse
from digital_backend.mock_store import mock_db

router = APIRouter(prefix="/profile", tags=["13. App Customer Profile (v2)"])


@router.get("", response_model=ApiResponse[CustomerProfileResponse], summary="Get Customer Profile Details")
async def get_customer_profile(cif: str = "CIF100001"):
    """
    Fetches the logged-in customer's comprehensive profile details including KYC status,
    registered mobile, PAN, masked Aadhaar, home branch, and communication preferences.
    """
    customer = mock_db.customers.get(cif)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "CUSTOMER_NOT_FOUND", "message": f"Customer with CIF {cif} not found"}
        )

    # Count registered accounts belonging to this customer
    account_count = sum(1 for acc in mock_db.accounts.values() if acc.get("cif") == cif)

    profile_data = CustomerProfileResponse(
        cif=customer["cif"],
        full_name=customer["name"],
        customer_type=customer["customer_type"],
        email=customer["email"],
        mobile_number=customer["mobile_number"],
        pan_number=customer["pan_number"],
        aadhaar_masked=customer["aadhaar_masked"],
        date_of_birth=customer.get("dob_or_incorporation", "1992-05-14"),
        gender=customer.get("gender", "MALE"),
        address=customer["address"],
        kyc_status=customer["kyc_status"],
        kyc_verified_on=customer.get("kyc_verified_on", "2024-01-16"),
        digital_profile_status=customer.get("digital_profile_status", "ACTIVE"),
        home_branch=customer.get("home_branch", "Nariman Point (001)"),
        avatar_url=customer.get("avatar_url", "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150"),
        communication_preferences={
            "email_alerts": True,
            "sms_alerts": True,
            "push_notifications": True,
            "whatsapp_alerts": True
        },
        last_login=customer.get("last_login", "Today, 09:42 AM"),
        registered_accounts_count=account_count or 3
    )

    return ApiResponse(data=profile_data, message="Customer profile retrieved successfully")

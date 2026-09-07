from fastapi import APIRouter, HTTPException, status
from digital_backend.schemas.common import ApiResponse, BaseApiResponse
from digital_backend.schemas.flutter_schemas import (
    MpinVerifyRequest,
    MpinSetRequest,
    BiometricVerifyRequest,
    BiometricRegisterRequest,
    OtpSendRequest,
    OtpVerifyRequest,
    CustomerLoginRequest,
    CustomerRegisterRequest,
    AuthSessionData
)
from digital_backend.mock_store import mock_db
import uuid

router = APIRouter(prefix="/auth", tags=["2. App Auth & Security"])

@router.post("/login", response_model=ApiResponse[AuthSessionData], summary="Customer Quick Login (MPIN / Credentials)")
async def customer_login(payload: CustomerLoginRequest):
    """
    Standard Mobile App Login endpoint.
    - If `mpin` is passed (default daily mobile flow), it validates the 4/6-digit MPIN without asking for a password.
    - If `password` is explicitly passed (e.g. internet banking fallback), it authenticates via password.
    """
    # 1. MPIN Login Flow
    if payload.mpin:
        if payload.mpin not in ["1234", "0000", "5678"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "INVALID_MPIN", "message": "Invalid MPIN. 2 attempts remaining."}
            )
        customer = mock_db.customers.get("CIF100001")
        session = AuthSessionData(
            cif=customer["cif"],
            customer_name=customer["name"],
            customer_type=customer["customer_type"],
            email=customer["email"],
            mobile_number=customer["mobile_number"],
            last_login_at=customer["last_login"],
            access_token=f"jwt_mock_token_{uuid.uuid4().hex[:12]}",
            token_type="Bearer",
            expires_in_seconds=86400
        )
        return ApiResponse(data=session, message="Login successful via MPIN")

    # 2. Password Fallback Flow
    customer = mock_db.customers.get("CIF100001")
    session = AuthSessionData(
        cif=customer["cif"],
        customer_name=customer["name"],
        customer_type=customer["customer_type"],
        email=customer["email"],
        mobile_number=customer["mobile_number"],
        last_login_at=customer["last_login"],
        access_token=f"jwt_mock_token_{uuid.uuid4().hex[:12]}",
        token_type="Bearer",
        expires_in_seconds=86400
    )
    return ApiResponse(data=session, message="Login successful")


@router.post("/mpin/verify", response_model=ApiResponse[AuthSessionData], summary="Direct MPIN Verification & Quick Unlock")
async def verify_mpin(payload: MpinVerifyRequest):
    """
    Direct 4/6-digit MPIN verification for instant customer app unlock (No password required).
    """
    if payload.mpin not in ["1234", "0000", "5678"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_MPIN", "message": "Invalid MPIN. 2 attempts remaining."}
        )
    customer = mock_db.customers.get(payload.cif or "CIF100001", mock_db.customers["CIF100001"])
    session = AuthSessionData(
        cif=customer["cif"],
        customer_name=customer["name"],
        customer_type=customer["customer_type"],
        email=customer["email"],
        mobile_number=customer["mobile_number"],
        last_login_at=customer["last_login"],
        access_token=f"jwt_mock_token_{uuid.uuid4().hex[:12]}"
    )
    return ApiResponse(data=session, message="MPIN verified successfully")


@router.post("/mpin/set", response_model=BaseApiResponse, summary="Set or Change MPIN")
async def set_mpin(payload: MpinSetRequest):
    """
    Set a new MPIN or change existing MPIN with OTP verification.
    """
    if payload.new_mpin != payload.confirm_mpin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "MPIN_MISMATCH", "message": "New MPIN and Confirmation MPIN do not match."}
        )
    return BaseApiResponse(success=True, response_code="BB-200", message="MPIN updated successfully")


@router.post("/biometric/verify", response_model=ApiResponse[AuthSessionData], summary="Direct Biometric Unlock (Fingerprint / FaceID)")
async def verify_biometric(payload: BiometricVerifyRequest):
    """
    Direct hardware biometric unlock for instant app access (No password required).
    """
    customer = mock_db.customers.get(payload.cif or "CIF100001", mock_db.customers["CIF100001"])
    session = AuthSessionData(
        cif=customer["cif"],
        customer_name=customer["name"],
        customer_type=customer["customer_type"],
        email=customer["email"],
        mobile_number=customer["mobile_number"],
        last_login_at=customer["last_login"],
        access_token=f"jwt_mock_token_{uuid.uuid4().hex[:12]}"
    )
    return ApiResponse(data=session, message="Biometric authentication successful")


@router.post("/biometric/register", response_model=BaseApiResponse, summary="Register Biometric Device Key")
async def register_biometric(payload: BiometricRegisterRequest):
    """
    Enrolls device public key / hardware security enclave for biometric login.
    """
    return BaseApiResponse(
        success=True,
        response_code="BB-200",
        message=f"Biometric device '{payload.device_name}' successfully enrolled."
    )


@router.post("/otp/send", response_model=ApiResponse[dict], summary="Trigger OTP to Registered Mobile Number")
async def send_otp(payload: OtpSendRequest):
    """
    Dispatches OTP for transaction confirmation, login, or beneficiary registration.
    """
    ref_no = f"OTP-{uuid.uuid4().hex[:6].upper()}"
    return ApiResponse(
        data={
            "otp_reference": ref_no,
            "masked_mobile": "XXXXXX3210",
            "expiry_seconds": 180,
            "demo_otp_hint": "123456"
        },
        message="OTP sent to your registered mobile number"
    )


@router.post("/otp/verify", response_model=BaseApiResponse, summary="Verify OTP Code")
async def verify_otp(payload: OtpVerifyRequest):
    """
    Validates received OTP against the given reference.
    """
    if payload.otp_code not in ["123456", "000000"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_OTP", "message": "Invalid or expired OTP"}
        )
    return BaseApiResponse(success=True, response_code="BB-200", message="OTP verified successfully")


@router.post("/register", response_model=ApiResponse[AuthSessionData], summary="Self-Service Customer Registration")
async def register_customer(payload: CustomerRegisterRequest):
    """
    Self-service digital onboarding validating KYC/CIF records.
    """
    session = AuthSessionData(
        cif=payload.cif,
        customer_name="Arjun Mehta",
        customer_type="RETAIL",
        email=payload.email,
        mobile_number=payload.mobile_number,
        last_login_at="Just now",
        access_token=f"jwt_mock_token_{uuid.uuid4().hex[:12]}"
    )
    return ApiResponse(data=session, message="Registration completed successfully. Welcome to Bharat Bank!")


@router.post("/forgot-password", response_model=BaseApiResponse, summary="Forgot Password / Reset Request")
async def forgot_password(login_id: str = "arjun.mehta"):
    """
    Initiate account password recovery via OTP.
    """
    return BaseApiResponse(
        success=True,
        response_code="BB-200",
        message=f"Password reset link and OTP instructions sent to registered contact info for '{login_id}'."
    )

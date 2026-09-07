from fastapi import APIRouter
from digital_backend.schemas.common import ApiResponse
from digital_backend.schemas.flutter_schemas import (
    AppVersionResponse,
    ThemeConfigResponse,
    BranchAtmItem,
    SubsystemHealth
)
from digital_backend.mock_store import mock_db

router = APIRouter(tags=["1. App System & Config"])

@router.get("/version", response_model=ApiResponse[AppVersionResponse], summary="Get Backend Version & System Health")
async def get_app_version():
    """
    Returns app version, backend build details, minimum supported mobile client versions, 
    and real-time downstream health status (CBS, Switch, BBPS, SMS Gateway).
    """
    data = AppVersionResponse(
        app_name="Bharat Bank Mobile",
        app_version="2.4.0",
        build_number=240,
        backend_version="1.0.0",
        min_supported_version="2.0.0",
        force_update_required=False,
        server_status="HEALTHY",
        environment="production-mock",
        subsystems=[
            SubsystemHealth(name="CBS (Core Banking System)", status="UP", latency_ms=14.2),
            SubsystemHealth(name="NPST Payment Switch (IMPS/NEFT/RTGS)", status="UP", latency_ms=8.5),
            SubsystemHealth(name="NPCI BBPS Gateway", status="UP", latency_ms=22.1),
            SubsystemHealth(name="SMS & Email Notification Service", status="UP", latency_ms=5.0)
        ]
    )
    return ApiResponse(data=data, message="System status healthy")


@router.get("/theme", response_model=ApiResponse[ThemeConfigResponse], summary="Get Dynamic Theme Configuration")
async def get_app_theme():
    """
    Sends theme configuration including:
    - 3 primary colors for light mode
    - 3 primary colors for dark mode
    - `is_dark_mode_configured` boolean flag
    - Typography details (Font families, scaling)
    - Logo URLs (light, dark, standard, favicon)
    - Optimized dynamic schema for client rendering.
    """
    return ApiResponse(
        data=ThemeConfigResponse(**mock_db.theme_config),
        message="Theme configuration retrieved successfully"
    )


@router.get("/branches-atms", response_model=ApiResponse[list[BranchAtmItem]], summary="Get Nearby Branches & ATMs")
async def get_branches_and_atms():
    """
    Returns list of nearby Bharat Bank branches, ATMs, and Cash Deposit Machines with geo coordinates and service details.
    """
    items = [
        BranchAtmItem(
            id="BR-001",
            type="BRANCH",
            name="Bharat Bank - Nariman Point Branch",
            address="102, Maker Chambers V, Nariman Point, Mumbai 400021",
            city="Mumbai",
            ifsc_code="APEX0001048",
            contact_phone="+91 22 2288 9900",
            latitude=18.9272,
            longitude=72.8228,
            distance_km=1.2,
            operating_hours="10:00 AM - 04:30 PM (Mon-Sat)",
            services_available=["Locker Facility", "Forex Desk", "Cash Deposit Machine", "Cheque Drop Box"],
            is_open_now=True
        ),
        BranchAtmItem(
            id="ATM-002",
            type="ATM",
            name="Bharat Bank 24x7 ATM - Bandra West",
            address="Ground Floor, Hill Road, Bandra West, Mumbai 400050",
            city="Mumbai",
            ifsc_code=None,
            contact_phone=None,
            latitude=19.0558,
            longitude=72.8347,
            distance_km=0.8,
            operating_hours="24 Hours Open",
            services_available=["Cash Withdrawal", "PIN Change", "Mini Statement"],
            is_open_now=True
        )
    ]
    return ApiResponse(data=items, message="Nearby locations fetched")

from fastapi import APIRouter
from digital_backend.schemas.common import ApiResponse, BaseApiResponse
from digital_backend.schemas.flutter_schemas import ThemeConfigResponse
from digital_backend.schemas.admin_schemas import AdminThemeUpdateRequest
from digital_backend.mock_store import mock_db

router = APIRouter(prefix="/theme-config", tags=["6. Admin Dynamic App Theme & Branding"])

@router.get("", response_model=ApiResponse[ThemeConfigResponse], summary="Get Current Mobile Dynamic Theme")
async def get_theme_configuration():
    """
    View currently active mobile app dynamic styling, branding assets, and colors.
    """
    return ApiResponse(data=ThemeConfigResponse(**mock_db.theme_config), message="Current theme configuration")


@router.put("", response_model=ApiResponse[ThemeConfigResponse], summary="Update Mobile Dynamic Theme")
async def update_theme_configuration(payload: AdminThemeUpdateRequest):
    """
    Real-time push of branding colors, light/dark themes, and logo assets to mobile clients.
    """
    mock_db.theme_config.update(payload.dict())
    
    # Audit log
    mock_db.audit_logs.insert(0, {
        "log_id": f"AUDIT-THEME-UPDATE",
        "timestamp": "2026-09-07T06:30:00Z",
        "admin_user": "rajesh.amin",
        "action_type": "DYNAMIC_THEME_UPDATE",
        "target_resource_id": payload.theme_id,
        "ip_address": "10.20.4.115",
        "status": "SUCCESS"
    })
    
    return ApiResponse(data=ThemeConfigResponse(**mock_db.theme_config), message="App theme configuration updated in real-time")

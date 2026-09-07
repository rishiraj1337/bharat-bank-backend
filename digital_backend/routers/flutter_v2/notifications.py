from fastapi import APIRouter, HTTPException, status
from typing import List
from digital_backend.schemas.common import ApiResponse, BaseApiResponse
from digital_backend.schemas.flutter_schemas import NotificationItem
from digital_backend.mock_store import mock_db

router = APIRouter(prefix="/notifications", tags=["14. App Notifications & Alerts (v2)"])


@router.get("", response_model=ApiResponse[List[NotificationItem]], summary="List Customer In-App Notifications")
async def list_notifications(cif: str = "CIF100001"):
    """
    Retrieves chronological stream of in-app notifications for transactions,
    security events, utility bill dues, and promotional offers.
    """
    user_notifs = [n for n in mock_db.notifications if n.get("cif") == cif or not n.get("cif")]
    items = [NotificationItem(**n) for n in user_notifs]
    return ApiResponse(data=items, message=f"Retrieved {len(items)} notifications")


@router.put("/{notification_id}/read", response_model=BaseApiResponse, summary="Mark Notification as Read")
async def mark_notification_read(notification_id: str):
    """
    Marks a specific notification as read in the customer inbox.
    """
    found = False
    for n in mock_db.notifications:
        if n["notification_id"] == notification_id:
            n["is_read"] = True
            found = True
            break

    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOTIFICATION_NOT_FOUND", "message": f"Notification {notification_id} not found"}
        )

    return BaseApiResponse(
        success=True,
        response_code="BB-200",
        message=f"Notification '{notification_id}' marked as read successfully"
    )

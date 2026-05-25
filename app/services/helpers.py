from app.utils.enums import DeliveryStatus

STATUS_BADGE_MAP = {
    DeliveryStatus.CREATED: "secondary",
    DeliveryStatus.ASSIGNED: "info",
    DeliveryStatus.PICKED_UP: "primary",
    DeliveryStatus.IN_TRANSIT: "warning",
    DeliveryStatus.DELIVERED: "success",
    DeliveryStatus.FAILED: "danger",
}

def badge_class(status: str) -> str:
    try:
        return STATUS_BADGE_MAP[DeliveryStatus(status)]
    except Exception:
        return "secondary"

from datetime import datetime

from app.extensions import db
from app.models.status_log import DeliveryStatusLog
from app.utils.enums import ALLOWED_TRANSITIONS, DeliveryStatus


def get_current_status(delivery):
    """
    Returns the latest status for a delivery.
    """
    if not delivery.status_logs:
        return None

    return max(
        delivery.status_logs,
        key=lambda log: log.status_timestamp
    ).status


def get_allowed_next_statuses(delivery):
    current_status = get_current_status(delivery)
    if current_status is None:
        return [DeliveryStatus.CREATED]

    return sorted(
        ALLOWED_TRANSITIONS.get(current_status, set()),
        key=lambda status: status.value,
    )


def apply_status_update(delivery, new_status):
    """
    Apply a status update if valid.
    Raises ValueError if transition is invalid.
    """
    current_status = get_current_status(delivery)

    if current_status is None:
        if new_status != DeliveryStatus.CREATED:
            raise ValueError("First status must be CREATED")
    else:
        allowed = ALLOWED_TRANSITIONS.get(current_status, set())
        if new_status not in allowed:
            raise ValueError(
                f"Invalid transition: {current_status.name} -> {new_status.name}"
            )

    log = DeliveryStatusLog(
        delivery_id=delivery.id,
        status=new_status
    )
    db.session.add(log)

    if new_status in {DeliveryStatus.DELIVERED, DeliveryStatus.FAILED}:
        delivery.completed_at = datetime.utcnow()

    db.session.commit()
    return log

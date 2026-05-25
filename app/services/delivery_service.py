from app.models.delivery import Delivery
from app.services.delivery_workflow import apply_status_update
from app.utils.enums import ALLOWED_TRANSITIONS, DeliveryStatus


class DeliveryService:

    @staticmethod
    def get_current_status(delivery: Delivery) -> DeliveryStatus | None:
        if not delivery.status_logs:
            return None
        return DeliveryStatus(delivery.status_logs[0].status)

    @staticmethod
    def can_transition(current: DeliveryStatus, next_status: DeliveryStatus) -> bool:
        return next_status in ALLOWED_TRANSITIONS.get(current, set())

    @staticmethod
    def update_status(delivery: Delivery, next_status: DeliveryStatus):
        return apply_status_update(delivery, next_status)

from enum import Enum

class DeliveryStatus(str, Enum):
    CREATED = "CREATED"
    ASSIGNED = "ASSIGNED"
    PICKED_UP = "PICKED_UP"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"

# Allowed transitions (state machine)
ALLOWED_TRANSITIONS = {
    DeliveryStatus.CREATED: {DeliveryStatus.ASSIGNED},
    DeliveryStatus.ASSIGNED: {DeliveryStatus.PICKED_UP},
    DeliveryStatus.PICKED_UP: {DeliveryStatus.IN_TRANSIT},
    DeliveryStatus.IN_TRANSIT: {DeliveryStatus.DELIVERED, DeliveryStatus.FAILED},
    DeliveryStatus.DELIVERED: set(),
    DeliveryStatus.FAILED: set(),
}

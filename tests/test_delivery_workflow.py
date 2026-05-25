import pytest

from app.extensions import db
from app.models.delivery import Delivery
from app.models.order import Order
from app.services.delivery_workflow import apply_status_update, get_allowed_next_statuses
from app.utils.enums import DeliveryStatus


@pytest.fixture()
def delivery(sample_data):
    order = Order(
        order_reference="ORD-2001",
        customer_id=sample_data["customer"].id,
        hub_id=sample_data["hub"].id,
    )
    db.session.add(order)
    db.session.flush()

    delivery = Delivery(order_id=order.id, partner_id=sample_data["partner"].id)
    db.session.add(delivery)
    db.session.commit()
    return delivery


def test_delivery_status_transitions_are_guarded(delivery):
    assert get_allowed_next_statuses(delivery) == [DeliveryStatus.CREATED]

    apply_status_update(delivery, DeliveryStatus.CREATED)
    apply_status_update(delivery, DeliveryStatus.ASSIGNED)

    with pytest.raises(ValueError):
        apply_status_update(delivery, DeliveryStatus.DELIVERED)

    apply_status_update(delivery, DeliveryStatus.PICKED_UP)
    apply_status_update(delivery, DeliveryStatus.IN_TRANSIT)
    apply_status_update(delivery, DeliveryStatus.DELIVERED)

    assert delivery.completed_at is not None

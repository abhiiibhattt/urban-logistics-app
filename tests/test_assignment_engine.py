from app.extensions import db
from app.models.order import Order
from app.services.assignment_engine import assign_delivery
from app.services.delivery_workflow import get_current_status
from app.utils.enums import DeliveryStatus


def test_assign_delivery_uses_available_partner(sample_data):
    order = Order(
        order_reference="ORD-1001",
        customer_id=sample_data["customer"].id,
        hub_id=sample_data["hub"].id,
    )
    db.session.add(order)
    db.session.commit()

    delivery = assign_delivery(order)

    assert delivery is not None
    assert delivery.partner_id == sample_data["partner"].id
    assert get_current_status(delivery) == DeliveryStatus.ASSIGNED


def test_assign_delivery_returns_none_when_partner_at_capacity(sample_data):
    sample_data["partner"].max_active_deliveries = 0
    order = Order(
        order_reference="ORD-1002",
        customer_id=sample_data["customer"].id,
        hub_id=sample_data["hub"].id,
    )
    db.session.add(order)
    db.session.commit()

    assert assign_delivery(order) is None

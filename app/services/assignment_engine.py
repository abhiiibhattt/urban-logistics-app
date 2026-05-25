from app.extensions import db
from app.models.delivery import Delivery
from app.models.partner import DeliveryPartner
from app.models.status_log import DeliveryStatusLog
from app.utils.enums import DeliveryStatus
from datetime import datetime, timedelta


def assign_delivery(order):
    """
    Auto-assign best available delivery partner for an order.
    Returns Delivery or None.
    """

    # Find eligible partners for the order's hub
    partners = (
        DeliveryPartner.query
        .filter_by(
            hub_id=order.hub_id,
            is_active=True
        )
        .all()
    )

    if not partners:
        return None

    # Filter partners under capacity
    eligible = []
    for partner in partners:
        active_count = Delivery.query.filter(
            Delivery.partner_id == partner.id,
            Delivery.completed_at.is_(None)
        ).count()

        if active_count < partner.max_active_deliveries:
            eligible.append((partner, active_count))

    if not eligible:
        return None

    # Choose least-loaded partner
    eligible.sort(key=lambda x: x[1])
    selected_partner = eligible[0][0]

    # Create delivery
    delivery = Delivery(
        order_id=order.id,
        partner_id=selected_partner.id
    )
    db.session.add(delivery)
    db.session.flush()

    created_at = datetime.utcnow()

    # Record the full lifecycle start so later transitions remain valid.
    db.session.add(
        DeliveryStatusLog(
            delivery_id=delivery.id,
            status=DeliveryStatus.CREATED,
            status_timestamp=created_at,
        )
    )
    db.session.add(
        DeliveryStatusLog(
            delivery_id=delivery.id,
            status=DeliveryStatus.ASSIGNED,
            status_timestamp=created_at + timedelta(microseconds=1),
        )
    )

    db.session.commit()

    return delivery

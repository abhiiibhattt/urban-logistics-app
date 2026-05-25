from flask import Blueprint, render_template
from app.models.order import Order
from app.models.delivery import Delivery
from app.models.partner import DeliveryPartner
from app.services.delivery_service import DeliveryService

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def dashboard():
    # KPIs
    total_orders = Order.query.count()

    active_deliveries = (
        Delivery.query
        .filter(Delivery.completed_at.is_(None))
        .count()
    )

    active_partners = (
        DeliveryPartner.query
        .filter_by(is_active=True)
        .count()
    )

    # Recent deliveries (derived status)
    deliveries = (
        Delivery.query
        .order_by(Delivery.assigned_at.desc())
        .limit(5)
        .all()
    )

    recent_deliveries = []
    for delivery in deliveries:
        status = DeliveryService.get_current_status(delivery)
        recent_deliveries.append({
            "delivery": delivery,
            "order_ref": delivery.order.order_reference,
            "partner_name": delivery.partner.name,
            "status": status,
        })

    return render_template(
        "dashboard.html",
        total_orders=total_orders,
        active_deliveries=active_deliveries,
        active_partners=active_partners,
        recent_deliveries=recent_deliveries,
    )

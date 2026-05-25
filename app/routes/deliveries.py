from flask import Blueprint, render_template, request, jsonify
from app.extensions import db
from app.models.delivery import Delivery
from app.models.status_log import DeliveryStatusLog
from app.utils.enums import DeliveryStatus
from app.services.delivery_workflow import (
    apply_status_update,
    get_allowed_next_statuses,
    get_current_status,
)

deliveries_bp = Blueprint("deliveries", __name__)


@deliveries_bp.route("/<int:delivery_id>")
def detail(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)

    status_logs = (
        DeliveryStatusLog.query
        .filter_by(delivery_id=delivery.id)
        .order_by(DeliveryStatusLog.status_timestamp.desc())
        .all()
    )

    return render_template(
        "deliveries/detail.html",
        delivery=delivery,
        status_logs=status_logs,
        current_status=get_current_status(delivery),
        allowed_next_statuses=get_allowed_next_statuses(delivery),
        all_statuses=DeliveryStatus
    )


@deliveries_bp.route("/")
def list_deliveries():
    deliveries = (
        Delivery.query
        .order_by(Delivery.assigned_at.desc())
        .all()
    )

    rows = []
    for delivery in deliveries:
        rows.append({
            "delivery": delivery,
            "status": get_current_status(delivery),
        })

    return render_template("deliveries/list.html", rows=rows)


@deliveries_bp.route("/<int:delivery_id>/status/json", methods=["POST"])
def update_status_json(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    payload = request.get_json()

    try:
        new_status = DeliveryStatus[payload["status"]]
        log = apply_status_update(delivery, new_status)

        return jsonify({
            "success": True,
            "status": log.status.name,
            "timestamp": log.status_timestamp.isoformat()
        })

    except (KeyError, ValueError) as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

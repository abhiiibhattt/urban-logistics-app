from flask import Blueprint, redirect, render_template, url_for, flash
from app.models.delivery import Delivery
from app.models.partner import DeliveryPartner
from app.services.partner_service import PartnerService

partners_bp = Blueprint("partners", __name__)


@partners_bp.route("/")
def list_partners():
    partners = DeliveryPartner.query.order_by(DeliveryPartner.name).all()

    rows = []
    for partner in partners:
        active_deliveries = (
            Delivery.query
            .filter_by(partner_id=partner.id, completed_at=None)
            .count()
        )
        rows.append({
            "partner": partner,
            "active_deliveries": active_deliveries,
        })

    return render_template("partners/list.html", rows=rows)


@partners_bp.route("/<int:partner_id>/activate", methods=["POST"])
def activate_partner(partner_id):
    try:
        PartnerService.activate_partner(partner_id)
        flash("Partner activated", "success")
    except ValueError as exc:
        flash(str(exc), "error")

    return redirect(url_for("dashboard.dashboard"))


@partners_bp.route("/<int:partner_id>/deactivate", methods=["POST"])
def deactivate_partner(partner_id):
    try:
        PartnerService.deactivate_partner(partner_id)
        flash("Partner deactivated", "success")
    except ValueError as exc:
        flash(str(exc), "error")

    return redirect(url_for("dashboard.dashboard"))

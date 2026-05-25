from app.extensions import db
from app.models.partner import DeliveryPartner
from app.models.delivery import Delivery


class PartnerService:
    """
    Service layer for delivery partner lifecycle management.

    Responsibilities:
    - Activate partners
    - Deactivate partners
    - Enforce operational safety rules
    """

    @staticmethod
    def activate_partner(partner_id: int) -> DeliveryPartner:
        """
        Activate a delivery partner.
        """

        partner = DeliveryPartner.query.get(partner_id)
        if not partner:
            raise ValueError("Delivery partner not found")

        if partner.is_active:
            return partner  # idempotent operation

        partner.is_active = True
        db.session.commit()

        return partner

    @staticmethod
    def deactivate_partner(partner_id: int) -> DeliveryPartner:
        """
        Deactivate a delivery partner.

        Business rules:
        - Partner must exist
        - Partner cannot be deactivated if they have active deliveries
        """

        partner = DeliveryPartner.query.get(partner_id)
        if not partner:
            raise ValueError("Delivery partner not found")

        active_deliveries = (
            Delivery.query
            .filter_by(partner_id=partner_id, completed_at=None)
            .count()
        )

        if active_deliveries > 0:
            raise ValueError(
                "Cannot deactivate partner with active deliveries"
            )

        partner.is_active = False
        db.session.commit()

        return partner

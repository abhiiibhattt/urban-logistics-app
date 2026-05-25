from app.extensions import db
from app.utils.enums import DeliveryStatus

class Delivery(db.Model):
    __tablename__ = "deliveries"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id"),
        nullable=False,
        unique=True,
    )
    partner_id = db.Column(
        db.Integer,
        db.ForeignKey("delivery_partners.id"),
        nullable=False,
    )
    assigned_at = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp(),
        nullable=False,
    )
    completed_at = db.Column(db.DateTime)

    order = db.relationship("Order", back_populates="delivery")
    partner = db.relationship("DeliveryPartner", back_populates="deliveries")
    status_logs = db.relationship(
        "DeliveryStatusLog",
        back_populates="delivery",
        order_by="desc(DeliveryStatusLog.status_timestamp)",
        cascade="all, delete-orphan",
    )

    def current_status(self):
        if not self.status_logs:
            return None
        return self.status_logs[0].status

from app.extensions import db

class DeliveryPartner(db.Model):
    __tablename__ = "delivery_partners"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

    hub_id = db.Column(
        db.Integer,
        db.ForeignKey("hubs.id"),
        nullable=False
    )

    is_active = db.Column(db.Boolean, default=True, nullable=False)
    max_active_deliveries = db.Column(db.Integer, default=3, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    hub = db.relationship("Hub", back_populates="partners")

    deliveries = db.relationship(
        "Delivery",
        back_populates="partner",
        lazy="dynamic"
    )

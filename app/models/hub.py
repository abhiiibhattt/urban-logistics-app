from app.extensions import db

class Hub(db.Model):
    __tablename__ = "hubs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    region_id = db.Column(
        db.Integer,
        db.ForeignKey("regions.id"),
        nullable=False
    )

    region = db.relationship("Region", back_populates="hubs")

    orders = db.relationship(
        "Order",
        back_populates="hub",
        lazy="dynamic"
    )

    partners = db.relationship(
        "DeliveryPartner",
        back_populates="hub",
        lazy="dynamic"
    )

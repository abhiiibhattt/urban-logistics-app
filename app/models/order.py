from app.extensions import db

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    order_reference = db.Column(db.String(50), nullable=False, unique=True)

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.id"),
        nullable=False
    )

    hub_id = db.Column(
        db.Integer,
        db.ForeignKey("hubs.id"),
        nullable=False
    )

    is_cancelled = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    customer = db.relationship("Customer", back_populates="orders")
    hub = db.relationship("Hub", back_populates="orders")

    delivery = db.relationship(
        "Delivery",
        back_populates="order",
        uselist=False
    )

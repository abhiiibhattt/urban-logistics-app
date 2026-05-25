from app.extensions import db

class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    orders = db.relationship(
        "Order",
        back_populates="customer",
        lazy="dynamic"
    )

from app.extensions import db
from app.utils.enums import DeliveryStatus

class DeliveryStatusLog(db.Model):
    __tablename__ = "delivery_status_logs"

    id = db.Column(db.Integer, primary_key=True)
    delivery_id = db.Column(
        db.Integer,
        db.ForeignKey("deliveries.id", ondelete="CASCADE"),
        nullable=False,
    )
    status = db.Column(db.Enum(DeliveryStatus), nullable=False)
    status_timestamp = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp(),
        nullable=False,
    )

    delivery = db.relationship("Delivery", back_populates="status_logs")

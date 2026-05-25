from app.extensions import db

class Region(db.Model):
    __tablename__ = "regions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    hubs = db.relationship(
        "Hub",
        back_populates="region",
        lazy="dynamic"
    )

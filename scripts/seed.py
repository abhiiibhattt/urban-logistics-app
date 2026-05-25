from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import create_app
from app.extensions import db
from app.models.customer import Customer
from app.models.hub import Hub
from app.models.partner import DeliveryPartner
from app.models.region import Region


def get_or_create(model, defaults=None, **filters):
    instance = model.query.filter_by(**filters).first()
    if instance:
        return instance

    params = {**filters, **(defaults or {})}
    instance = model(**params)
    db.session.add(instance)
    db.session.flush()
    return instance


def seed():
    app = create_app()
    with app.app_context():
        central = get_or_create(Region, name="Central")
        north = get_or_create(Region, name="North")

        central_hub = get_or_create(Hub, name="Central Hub", region_id=central.id)
        north_hub = get_or_create(Hub, name="North Hub", region_id=north.id)

        get_or_create(
            DeliveryPartner,
            name="Aarav Express",
            hub_id=central_hub.id,
            defaults={"max_active_deliveries": 3},
        )
        get_or_create(
            DeliveryPartner,
            name="Metro QuickShip",
            hub_id=central_hub.id,
            defaults={"max_active_deliveries": 2},
        )
        get_or_create(
            DeliveryPartner,
            name="Northline Couriers",
            hub_id=north_hub.id,
            defaults={"max_active_deliveries": 3},
        )

        get_or_create(
            Customer,
            phone_number="9000000001",
            defaults={"full_name": "Sample Customer", "email": "customer@example.com"},
        )

        db.session.commit()
        print("Seed data inserted.")


if __name__ == "__main__":
    seed()

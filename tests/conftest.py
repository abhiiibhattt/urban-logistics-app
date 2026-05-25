import pytest

from app import create_app
from app.config import TestConfig
from app.extensions import db
from app.models.customer import Customer
from app.models.hub import Hub
from app.models.partner import DeliveryPartner
from app.models.region import Region


@pytest.fixture()
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def sample_data(app):
    region = Region(name="Central")
    db.session.add(region)
    db.session.flush()

    hub = Hub(name="Central Hub", region_id=region.id)
    customer = Customer(
        full_name="Sample Customer",
        phone_number="9000000001",
        email="sample@example.com",
    )
    db.session.add_all([hub, customer])
    db.session.flush()

    partner = DeliveryPartner(
        name="Aarav Express",
        hub_id=hub.id,
        is_active=True,
        max_active_deliveries=3,
    )
    db.session.add(partner)
    db.session.commit()

    return {
        "region": region,
        "hub": hub,
        "customer": customer,
        "partner": partner,
    }

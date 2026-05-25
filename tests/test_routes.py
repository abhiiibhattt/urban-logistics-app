from app.models.delivery import Delivery
from app.models.order import Order


def test_dashboard_renders(client, sample_data):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Operations Dashboard" in response.data


def test_partners_page_renders(client, sample_data):
    response = client.get("/partners/")

    assert response.status_code == 200
    assert b"Delivery Partners" in response.data
    assert b"Aarav Express" in response.data


def test_order_creation_assigns_delivery(client, sample_data):
    response = client.post(
        "/orders/new",
        data={
            "order_reference": "ORD-3001",
            "customer_id": str(sample_data["customer"].id),
            "hub_id": str(sample_data["hub"].id),
        },
        follow_redirects=True,
    )

    order = Order.query.filter_by(order_reference="ORD-3001").one()
    delivery = Delivery.query.filter_by(order_id=order.id).one()

    assert response.status_code == 200
    assert delivery.partner_id == sample_data["partner"].id
    assert b"Order created and assigned successfully" in response.data

    deliveries_response = client.get("/deliveries/")
    assert deliveries_response.status_code == 200
    assert b"ORD-3001" in deliveries_response.data

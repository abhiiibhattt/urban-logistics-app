from app.extensions import db
from app.models.order import Order
from app.models.customer import Customer
from app.models.hub import Hub


class OrderService:
    """
    Service layer for order lifecycle management.

    Responsibilities:
    - Order creation
    - Order cancellation
    - Enforcing order-level business rules
    """

    @staticmethod
    def create_order(order_reference: str, customer_id: int, hub_id: int) -> Order:
        """
        Create a new order.

        Business rules:
        - Order reference must be unique
        - Customer must exist
        - Hub must exist
        """

        if Order.query.filter_by(order_reference=order_reference).first():
            raise ValueError("Order reference already exists")

        customer = Customer.query.get(customer_id)
        if not customer:
            raise ValueError("Customer not found")

        hub = Hub.query.get(hub_id)
        if not hub:
            raise ValueError("Hub not found")

        order = Order(
            order_reference=order_reference,
            customer_id=customer_id,
            hub_id=hub_id,
        )

        db.session.add(order)
        db.session.commit()

        return order

    @staticmethod
    def cancel_order(order_id: int) -> Order:
        """
        Cancel an existing order.

        Business rules:
        - Order must exist
        - Order cannot be cancelled if a delivery already exists
        """

        order = Order.query.get(order_id)
        if not order:
            raise ValueError("Order not found")

        if order.delivery:
            raise ValueError("Cannot cancel order with an active delivery")

        if order.is_cancelled:
            raise ValueError("Order is already cancelled")

        order.is_cancelled = True
        db.session.commit()

        return order

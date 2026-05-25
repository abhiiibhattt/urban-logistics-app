from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models.order import Order
from app.models.customer import Customer
from app.models.hub import Hub
from app.services.assignment_engine import assign_delivery

orders_bp = Blueprint("orders", __name__, template_folder="../templates/orders")


@orders_bp.route("/", methods=["GET"])
def list_orders():
    orders = (
        Order.query
        .join(Customer)
        .join(Hub)
        .order_by(Order.created_at.desc())
        .all()
    )
    return render_template("orders/list.html", orders=orders)


@orders_bp.route("/new", methods=["GET", "POST"])
def new_order():
    customers = Customer.query.order_by(Customer.full_name).all()
    hubs = Hub.query.order_by(Hub.name).all()

    if request.method == "POST":
        order_reference = request.form.get("order_reference")
        hub_id = request.form.get("hub_id")

        if Order.query.filter_by(order_reference=order_reference).first():
            flash("Order reference already exists", "error")
            return redirect(url_for("orders.new_order"))

        if not Hub.query.get(hub_id):
            flash("Selected hub was not found", "error")
            return redirect(url_for("orders.new_order"))

        # Existing or new customer
        customer_id = request.form.get("customer_id")
        new_customer_name = request.form.get("new_customer_name")
        new_customer_phone = request.form.get("new_customer_phone")
        new_customer_email = request.form.get("new_customer_email")

        if customer_id:
            customer = Customer.query.get(customer_id)
            if not customer:
                flash("Selected customer was not found", "error")
                return redirect(url_for("orders.new_order"))
        else:
            if not new_customer_name or not new_customer_phone:
                flash("Customer name and phone required", "error")
                return redirect(url_for("orders.new_order"))

            customer = Customer(
                full_name=new_customer_name,
                phone_number=new_customer_phone,
                email=new_customer_email
            )
            db.session.add(customer)
            db.session.flush()  # get customer.id

        # Create order
        order = Order(
            order_reference=order_reference,
            customer_id=customer.id,
            hub_id=hub_id
        )
        db.session.add(order)
        db.session.flush()
        db.session.commit()

        delivery = assign_delivery(order)
        if delivery:
            flash("Order created and assigned successfully", "success")
        else:
            flash("Order created, but no eligible partner is available", "error")
        return redirect(url_for("orders.list_orders"))

    return render_template(
        "orders/new.html",
        customers=customers,
        hubs=hubs
    )

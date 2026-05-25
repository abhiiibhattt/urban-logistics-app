from app.routes.dashboard import dashboard_bp
from app.routes.orders import orders_bp
from app.routes.deliveries import deliveries_bp
from app.routes.partners import partners_bp

def register_blueprints(app):
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(orders_bp, url_prefix="/orders")
    app.register_blueprint(deliveries_bp, url_prefix="/deliveries")
    app.register_blueprint(partners_bp, url_prefix="/partners")

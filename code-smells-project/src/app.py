from flask import Flask
from flask_cors import CORS

from src.config.settings import Settings
from src.models.database import get_db
from src.models.product_model import ProductModel
from src.models.user_model import UserModel
from src.models.order_model import OrderModel
from src.controllers.product_controller import ProductController
from src.controllers.user_controller import UserController
from src.controllers.order_controller import OrderController
from src.views.routes import create_routes
from src.middlewares.error_handler import register_error_handlers


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = Settings.SECRET_KEY
    CORS(app)

    # Initialize database
    db = get_db()

    # Initialize models
    product_model = ProductModel(db)
    user_model = UserModel(db)
    order_model = OrderModel(db)

    # Initialize controllers
    product_controller = ProductController(product_model)
    user_controller = UserController(user_model)
    order_controller = OrderController(order_model)

    # Register routes
    app.register_blueprint(create_routes(product_controller, order_controller, user_controller))

    # Register error handlers
    register_error_handlers(app)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host=Settings.HOST, port=Settings.PORT, debug=Settings.DEBUG)

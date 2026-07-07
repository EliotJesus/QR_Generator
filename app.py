from flask import Flask

from config import SECRET_KEY
from database import init_db

from routes.main_routes import main_bp
from routes.qr_routes import qr_bp
from routes.stats_routes import stats_bp


def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    init_db()

    app.register_blueprint(main_bp)
    app.register_blueprint(qr_bp)
    app.register_blueprint(stats_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
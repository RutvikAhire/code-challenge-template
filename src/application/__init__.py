from flask import Flask
from flask_executor import Executor
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from application.config import Config


db = SQLAlchemy()
executor = Executor()
ma = Marshmallow()


def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        db.init_app(app)
        executor.init_app(app)
        ma.init_app(app)

        from application.home.routes import HOME
        from application.ingest.routes import INGEST
        from application.analytics.routes import ANALYTICS
        from application.apis.weather_utils import api_bp as api

        app.register_blueprint(HOME)
        app.register_blueprint(INGEST)
        app.register_blueprint(ANALYTICS)
        app.register_blueprint(api, url_prefix='/api')

    return app

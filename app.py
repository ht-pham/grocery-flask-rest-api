import os
from flask import Flask
from flask_smorest import Api

from resources.item import blp as ItemBlueprint
from resources.dept import blp as DeptBlueprint
from db import db
import models

def create_app(db_url=None):
    flask_app = Flask(__name__)

    flask_app.config["PROPAGATE_EXCEPTIONS"] = True
    flask_app.config["API_TITLE"] = "Grocery Items REST API"
    flask_app.config["API_VERSION"] = "v1"

    flask_app.config["OPENAPI_VERSION"]="3.0.3"
    flask_app.config["OPENAPI_URL_PREFIX"] = "/"
    flask_app.config["OPENAPI_SWAGGER_UI_PATH"]="/swagger-ui"
    flask_app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(flask_app)
    
    api = Api(flask_app)

    with flask_app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(DeptBlueprint)
    return flask_app
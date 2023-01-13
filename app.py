from flask import Flask
from flask_smorest import Api

from resources.item import blp as ItemBlueprint
from resources.dept import blp as DeptBlueprint

flask_app = Flask(__name__)

flask_app.config["PROPAGATE_EXCEPTIONS"] = True
flask_app.config["API_TITLE"] = "Grocery Items REST API"
flask_app.config["API_VERSION"] = "v1"

flask_app.config["OPENAPI_VERSION"]="3.0.3"
flask_app.config["OPENAPI_URL_PREFIX"] = "/"
flask_app.config["OPENAPI_SWAGGER_UI_PATH"]="/swagger-ui"
flask_app.config["OPENAPI_URL_PREFIX"] = "/https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(flask_app)

api.register_blueprint(ItemBlueprint)
api.register_blueprint(DeptBlueprint)
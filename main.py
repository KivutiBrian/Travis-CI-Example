from flask import Flask,Blueprint,jsonify
from flask_restx import Api, Resource,fields
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager,create_access_token,create_refresh_token,jwt_required,get_jwt_identity

from configs.DbConfig import DevelopmentConfigs

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    }
}

app = Flask(__name__)
app.config.from_object(DevelopmentConfigs)
app.config["PROPAGATE_EXCEPTIONS"] = False
blueprint = Blueprint('taskApi',__name__,url_prefix='/api/v1')
api = Api(blueprint, title='TASK_MANAGEMENT_API', description="A simple task manager api", version='1.0',author="Gaideh",
                            doc='/doc',authorizations=authorizations)
app.register_blueprint(blueprint)
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

# models
from models.TaskModel import TaskModel
from models.UserModel import UserModel

@app.before_first_request
def create_tables():
    db.create_all()

#error handlers
from errors.handlers import *  

@app.route('/') #so hii message ndio itakuwa inatokea ukijaribu kuaccess api.
def home():
    return jsonify({"message":"This is a private API"})

from resources.Tasks import *
from resources.Users import *
from resources.RegistrationLogin import *




if __name__ == '__main__':
    app.run()

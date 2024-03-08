from flask import Flask
from flask_migrate import Migrate
from config import Config
from helpers import JSONEncoder
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from .site.routes import site
from .authentication.routes import auth
from .api.routes import api
from models import db, login_manager, User


app = Flask(__name__) #Application Factory?

CORS(app)
app.config.from_object(Config)
app.json_encoder = JSONEncoder
db.init_app(app)
login_manager.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)
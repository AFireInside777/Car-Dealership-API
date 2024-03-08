from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    print('Login Manager: User Loader was consulted. User_id: ' + user_id)
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(400), nullable=True, default='')
    last_name = db.Column(db.String(400), nullable=True, default='')
    email = db.Column(db.String(400), nullable=False)
    password = db.Column(db.String, nullable=True, default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, default='', unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, email, first_name='', last_name='',  password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def set_token(self, length):
        return secrets.token_hex(length)
    
    def __repr__(self):
        return f'User {self.email} has been added to the database'
    
class Car(db.Model):
    car_id = db.Column(db.String, primary_key=True)
    car_make = db.Column(db.String(300), nullable=False)
    car_body_type = db.Column(db.String(300), nullable=True)
    car_price = db.Column(db.String(100), nullable=False)
    car_year = db.Column(db.String(4), nullable=True)
    car_model = db.Column(db.String(300), nullable=False)
    car_fuel_type = db.Column(db.String(300), nullable=True)
    car_user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, car_body_type, car_year, car_fuel_type, car_user_token, car_make='',  car_price = '', car_model= ''):
        self.car_id = self.set_car_id()
        self.car_body_type = car_body_type
        self.car_year = car_year
        self.car_fuel_type = car_fuel_type
        self.car_user_token = car_user_token
        self.car_make = car_make
        self.car_price = car_price
        self.car_model = car_model
        
    def set_car_id(self):
        return (secrets.token_urlsafe())
    
    def __repr__(self):
        return f'The following cars have been added to the Cars table: {self.car_make} {self.car_model}'

class UserSchema(ma.Schema):
    class Meta:
        fields = ['id','first_name', 'last_name', 'email']

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class CarSchema(ma.Schema):
    class Meta:
        fields = ['car_id', 'car_year', 'car_make', 'car_model', 'car_price']

Car_schema = CarSchema()
Cars_schema = CarSchema(many=True)
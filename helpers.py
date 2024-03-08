from flask import json
from functools import wraps
import decimal
import secrets
from flask import request, jsonify, json 
from models import User

def token_required(flask_view):
    @wraps(flask_view)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split(' ')[1]
        if not token:
            return jsonify({'message': 'Token is missing.'}), 401
        
        try:
            current_user_token = User.query.filter_by(token = token).first()
            
        except:
            owner = User.query.filter_by(token = token).first()
            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({'message': 'Token is invalid'})

        return flask_view(current_user_token, *args, **kwargs)
    return decorated

class JSONEncoder(json.JSONEncoder):
    print("Encoder was used.")
    def default(self, obj):
        print("This is 'obj': " + str(obj))
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        print("This is 'default obj': " + super(JSONEncoder, self).default(obj))
        return super(JSONEncoder, self).default(obj)
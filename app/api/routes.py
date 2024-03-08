from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import User, Car, Car_schema, db, Cars_schema
import secrets

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/addcar', methods = ['POST'])
@token_required
def addcar(current_user_token):
    car_make = request.json['car_make']
    car_model = request.json['car_model']
    car_body_type = request.json['car_body_type']
    car_price = request.json['car_price']
    car_year = request.json['car_year']
    car_fuel_type = request.json['car_fuel_type']
    car_user_token = current_user_token.token

    print(f'The current User Token is: ' + current_user_token.token)

    car = Car(car_body_type, car_year, car_fuel_type, car_user_token, car_make, car_price, car_model)

    db.session.add(car)
    db.session.commit()

    response = Car_schema.dump(car)
    return jsonify(response)

@api.route('/getcars', methods = ['GET'])
@token_required
def getcars(current_user_token):
    cars = Car.query.filter_by(car_user_token = current_user_token.token).all()
    response = Cars_schema.dump(cars)
    return jsonify(response)


@api.route('/deletecars/<id>', methods = ['DELETE'])
@token_required
def deletecars(current_user_token, id):
    cars = Car.query.filter_by(car_id = id).first()
    if cars.car_user_token == current_user_token.token:
        print(f'The following selection will be deleted: {cars.car_make} {cars.car_model} {cars.car_year}')
        db.session.delete(cars)
        db.session.commit()

        response = Car_schema.dump(cars)
        return jsonify(response)
    else:
        return jsonify({'message': 'The token is not correct.'})
    
@api.route('/editcar/<id>', methods = ['PUT'])
@token_required
def editcar(current_user_token, id):
    caredit = Car.query.filter_by(car_id = id).first()
    if secrets.compare_digest(caredit.car_user_token, current_user_token.token):
        caredit.car_make = request.json['car_make']
        caredit.car_model = request.json['car_model']
        caredit.car_body_type = request.json['car_body_type']
        caredit.car_price = request.json['car_price']
        caredit.car_year = request.json['car_year']
        caredit.car_fuel_type = request.json['car_fuel_type']
        caredit.car_user_token = current_user_token.token

        db.session.add(caredit)
        db.session.commit()

        response = Car_schema.dump(caredit)
        return jsonify ({'message': 'Here is the new car entry: '}, response)
    else:
        return jsonify ({'message': "The token sent for this request does not match the car item."})

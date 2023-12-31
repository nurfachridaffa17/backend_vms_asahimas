from flask import request, jsonify, session
from . import app
import os
import json
import requests
from .user import create_user, get_all_user, get_user_by_id, update_user, delete_user, update_user_photo
from .masterCard import create_card, get_all_card, get_card_by_id, update_card, delete_card, get_card_not_use
from .usertype import create_usertype, get_all_usertype, get_usertype_by_id, update_usertype, delete_usertype
from flask_login import login_required
from .access_area import create_access_area, get_all_access_area, get_access_area_by_id, update_access_area, delete_access_area
from .transaction import create_transaction, get_all_transaction, get_transaction_by_id, transaction_check_out, delete_transaction
from .models import M_User, M_Card, M_UserType
from werkzeug.security import generate_password_hash
from .inviting import create_inviting, get_all_inviting, get_inviting_by_id, approved_inviting, not_approved_inviting, delete_inviting, hold_inviting
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from .cookies import update_cookies, get_all_cookies, get_cookies_by_id


def token_required(f):
    @wraps(f)  # This preserves the original function's metadata
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]  # Get the token from the Authorization header

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = M_User.query.get(data['user_id'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password =request.form.get('password')

    user = M_User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    payload = {
        'user_id' : user.id,
        'id_usertype' : user.id_usertype,
        'user_name' : user.name,
        'user_email' : user.email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token}), 200

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logout success'}), 200


@app.route('/api/v1/user/create', methods=['POST'])
def user_route():
    if request.method == 'POST':
        return create_user()

@app.route('/user', methods=['GET','PUT'])
def get_update_user():
    email = request.args.get('email')
    if email is None:
        return jsonify({'message': 'Missing user email parameter'}), 400
    if request.method == 'GET':
        return get_user_by_id(email)
    elif request.method == 'PUT':
        return update_user(email=email)

@app.route('/user/update', methods=['PUT'])
@token_required
def update_user_route_by_id(current_user):
    id = request.args.get('id')
    if id is None:
        return jsonify({'message': 'Missing user ID parameter'}), 400
    return update_user_photo(id=id)

@app.route('/api/v1/user/all', methods=['GET'])
def get_all_user_route():
    return get_all_user()

@app.route('/api/v1/user/delete', methods=['DELETE'])
def delete_user_route():
    id = request.args.get('id')
    if id is None:
        return jsonify({'message': 'Missing user ID parameter'}), 400
    return delete_user(id=id)

@app.route('/api/v1/card/create', methods=['POST'])
def get_create_card():
    if request.method == 'POST':
        return create_card()

@app.route('/api/v1/card/all', methods=['GET'])
def get_all_card_route():
    return get_all_card()

@app.route('/api/v1/card', methods=['GET','PUT'])
def get_update_card():
    id = request.args.get('id')
    if id is None:
        return jsonify({'message': 'Missing card ID parameter'}), 400
    if request.method == 'GET':
        return get_card_by_id(id)
    elif request.method == 'PUT':
        return update_card(id=id)
    
@app.route('/api/v1/card/not_use', methods=['GET'])
def get_card_not_activate():
    return get_card_not_use()

@app.route('/api/v1/card/delete', methods=['DELETE'])
def delete_card_route():
    id = request.args.get('id')
    if id is None:
        return jsonify({'message': 'Missing card ID parameter'}), 400
    return delete_card(id=id)

@app.route('/api/v1/usertype', methods=['POST'])
def get_user_type():
    if request.method == 'POST':
        return create_usertype()

@app.route('/api/v1/usertype/all', methods=['GET'])
def get_all_usertype_route():
    return get_all_usertype()

@app.route('/api/v1/usertype', methods=['GET','PUT'])
def get_update_usertype():
    id = request.args.get('id')
    if id is None:
        return jsonify({'message': 'Missing usertype ID parameter'}), 400
    if request.method == 'GET':
        return get_usertype_by_id(id)
    elif request.method == 'PUT':
        return update_usertype(id=id)

@app.route('/api/v1/usertype/delete', methods=['DELETE'])
def delete_usertype_route():
    id = request.args.get('id')
    if id is None:
        return jsonify({'message': 'Missing usertype ID parameter'}), 400
    return delete_usertype(id=id)

@app.route('/api/v1/access_area', methods=['POST'])
def get_access_area():
    if request.method == 'POST':
        return create_access_area()

@app.route('/api/v1/access_area/all', methods=['GET'])
def get_all_access_area_route():
    return get_all_access_area()

@app.route('/api/v1/access_area', methods=['GET','PUT'])
def get_update_access_area():
    id = request.args.get('id')
    if id is None:
        return jsonify({'message': 'Missing access_area ID parameter'}), 400
    if request.method == 'GET':
        return get_access_area_by_id(id)
    elif request.method == 'PUT':
        return update_access_area(id=id)

@app.route('/api/v1/access_area/delete', methods=['DELETE'])
def delete_access_area_route():
    id = request.args.get('id')
    if id is None:
        return jsonify({'message': 'Missing access_area ID parameter'}), 400
    return delete_access_area(id=id)

@app.route('/api/v1/transaction', methods=['POST'])
def get_transaction():
    if request.method == 'POST':
        return create_transaction()

@app.route('/api/v1/transaction/all', methods=['GET'])
def get_all_transaction_route():
    return get_all_transaction()

@app.route('/api/v1/transaction', methods=['GET','PUT'])
def get_update_transaction():
    id = request.args.get('id')
    if id is None:
        return jsonify({'message': 'Missing transaction ID parameter'}), 400
    if request.method == 'GET':
        return get_transaction_by_id(id)
    elif request.method == 'PUT':
        return transaction_check_out(id=id)

@app.route('/api/v1/transaction/delete', methods=['DELETE'])
def delete_transaction_route():
    id = request.args.get('id')
    if id is None:
        return jsonify({'message': 'Missing transaction ID parameter'}), 400
    return delete_transaction(id=id)


@app.route('/api/v1/create/inviting', methods=['POST'])
@token_required
def get_inviting(current_user):
    user_id = current_user.id
    if request.method == 'POST':
        return create_inviting(id_user=user_id)


@app.route('/api/v1/inviting/all', methods=['GET'])
def get_all_inviting_route():
    if request.method == 'GET':
        return get_all_inviting()


@app.route('/api/v1/inviting', methods=['GET'])
def get_update_inviting():
    id = request.args.get('id')
    if id is None:
        return jsonify({'message': 'Missing inviting ID parameter'}), 400
    if request.method == 'GET':
        return get_inviting_by_id(id)


@app.route('/api/v1/inviting/delete', methods=['DELETE'])
def delete_inviting_route(id):
    id = request.args.get('id')
    if id is None:
        return jsonify({'message': 'Missing inviting ID parameter'}), 400 

    return delete_inviting(id=id)


@app.route('/api/v1/inviting/accept', methods=['PUT'])
@token_required
def accept_inviting_route(current_user):
    user_id = current_user.id
    id = request.args.get('id')
    if id is None:
        return jsonify({'message': 'Missing inviting ID parameter'}), 400
    return approved_inviting(id=id, id_user=user_id)


@app.route('/api/v1/inviting/reject', methods=['PUT'])
@token_required
def reject_inviting_route(current_user):
    id = request.args.get('id')
    user_id = current_user.id
    if id is None:
        return jsonify({'message': 'Missing parameter ID'}), 400
    return not_approved_inviting(id=id, id_user=user_id)

@app.route('/api/v1/inviting/hold', methods=['PUT'])
@token_required
def hold_inviting_route(current_user):
    id = request.args.get('id')
    user_id = current_user.id
    if id is None:
        return jsonify({'message': 'Missing parameter ID'}), 400
    return hold_inviting(id=id, id_user=user_id)

@app.route('/api/v1/cookie', methods=['GET'])
def get_cookie_data():
    id = request.args.get('id')
    if id is None:
        return jsonify({'message': 'Missing parameter ID'}), 400
    return get_cookies_by_id(id)

@app.route('/api/v1/cookie/all', methods=['GET'])
def get_all_cookie_data():
    return get_all_cookies()

@app.route('/api/v1/cookie', methods=['PUT'])
def update_cookie_data():
    id = request.args.get('id')
    if id is None:
        return jsonify({'message': 'Missing parameter ID'}), 400
    return update_cookies(id)
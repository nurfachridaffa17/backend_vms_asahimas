from flask import request, jsonify
from . import app
import os
import json
import requests
from .user import create_user, get_all_user, get_user_by_id, update_user, delete_user
from .masterCard import create_card, get_all_card, get_card_by_id, update_card, delete_card
from .usertype import create_usertype, get_all_usertype, get_usertype_by_id, update_usertype, delete_usertype
from flask_login import login_required
from .access_area import create_access_area, get_all_access_area, get_access_area_by_id, update_access_area, delete_access_area
from .transaction import create_transaction, get_all_transaction, get_transaction_by_id, transaction_check_out 


@app.route('/api/v1/user/create', methods=['POST'])
def user_route():
    if request.method == 'POST':
        return create_user()

@app.route('/user', methods=['GET','PUT'])
def get_update_user():
    id = request.args.get('id')  # Get the id from the query parameters
    if id is None:
        return jsonify({'message': 'Missing user ID parameter'}), 400
    if request.method == 'GET':
        return get_user_by_id(id)
    elif request.method == 'PUT':
        return update_user(id=id)

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
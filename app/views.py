from flask import request, jsonify
from . import app
import os
import json
import requests
from .user import create_user, get_all_user, get_user_by_id, update_user, delete_user
from flask_login import login_required

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
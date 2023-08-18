from flask import request, jsonify
from . import app
import os
import json
import requests
from .user import create_user, get_all_user, get_user_by_id, update_user
from flask_login import login_required

# @app.route('/api/v1/login', methods=['POST'])
# def login():
#     return login()

@app.route('/api/v1/user', methods=['POST', 'GET', 'PUT'])
def user_route():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        username = request.form.get('username')
        company = request.form.get('company')
        nik = request.form.get('nik')

        return create_user(email=email, name=name, password=password, username=username, company=company, nik=nik)
    
    # elif request.method == 'GET':
    #     return get_all_user()
    
#     elif request.method == 'PUT':
#         return update_user()

# @app.route('/api/v1/user/<id>', methods=['GET'])
# def user_by_id_route(id):
#     if request.method == 'GET':
#         return get_user_by_id(id)
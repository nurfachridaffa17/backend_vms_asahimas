from .models import db,M_User,Zkteco
from flask import request, jsonify, session
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os
from . import app
import base64
import json
import requests

def get_user_folder_path(user_id):
    return os.path.join(app.config['UPLOAD_FOLDER'], str(user_id))

def create_user(created_user):
    now = datetime.datetime.now()
    new_user = M_User(
        email = request.form.get('email'),
        password = generate_password_hash(request.form.get('password'), method='scrypt'),
        created_at = now,
        name = request.form.get('name'),
        username = request.form.get('username'),
        company = request.form.get('company'),
        id_usertype = request.form.get('id_usertype'),
        photo = None,
        nik = None,
        other_document = None,
        supervisor = created_user
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'}), 200


def update_user(email):
    user = M_User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'No user found!'}), 404

    get_id_user = M_User.query.filter_by(email=email).first()
    
    user_folder = get_user_folder_path(get_id_user.id)
    os.makedirs(user_folder, exist_ok=True)

    try:
        user.name = request.form.get('name')
        user.username = request.form.get('username')
        user.password = generate_password_hash(request.form.get('password'), method='scrypt')
        user.company = request.form.get('company')
        photo = request.files['photo']
        nik = request.files['nik']
        other_document = request.files['other_document']

        if 'photo' in request.files:
            photo.save(os.path.join(user_folder, photo.filename))
            save_photo = user_folder + '/' + photo.filename
            user.photo = save_photo
        
        if 'nik' in request.files:
            nik.save(os.path.join(user_folder, nik.filename))
            save_nik = user_folder + '/' + nik.filename
            user.nik = save_nik
        
        if 'other_document' in request.files:
            other_document.save(os.path.join(user_folder, other_document.filename))
            save_other_document = user_folder + '/' + other_document.filename
            user.other_document = save_other_document
        
        file_path_image = os.path.join(user_folder, photo.filename)
        with open(file_path_image, "rb") as img_file:
            my_string = base64.b64encode(img_file.read())
        user.photo_base64 = str(my_string.decode('utf-8'))
        
        db.session.commit()

        return jsonify({'message': "Success save"}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


def update_user_photo(id):
    url = app.config['URL_ENDPOINT'] + "/person/updatePersonnelPhoto"

    user = M_User.query.filter_by(id=id).first()

    user_folder = get_user_folder_path(user.id)
    os.makedirs(user_folder, exist_ok=True)

    photo = request.files['photo']

    if 'photo' in request.files:
        photo.save(os.path.join(user_folder, photo.filename))
        save_photo = user_folder + '/' + photo.filename
        user.photo = save_photo

    file_path_image = os.path.join(user_folder, photo.filename)
    with open(file_path_image, "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
    user.photo_base64 = str(my_string.decode('utf-8'))
    photo_user = str(my_string.decode('utf-8'))

    payload = json.dumps({
        "personPhoto" : photo_user,
        "pin": user.id
    })

    cookie = Zkteco.query.first()

    headers = {
        'Cookie' : cookie.cookie,
        'Content-Type' : 'application/json'
    }

    try:
        data = requests.post(url, headers=headers, data=payload)
        if data.status_code == 200:
            data = data.json()
            if data["message"] != "success":
                return jsonify({
                    'code' : data["code"],
                    'message': data["message"]
                    }), 500
            else:
                db.session.commit()
                return jsonify({
                    'code' : data["code"],
                    'message': data["message"]
                }), 200

        else:
            return jsonify({
                'code': data.status_code,
            }), data.status_code
    except Exception as e:
        return jsonify({'message': str(e)}), 500 


def get_all_user():
    users = M_User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['email'] = user.email
        user_data['password'] = user.password
        user_data['created_at'] = user.created_at
        user_data['supervisor'] = user.supervisor
        user_data['name'] = user.name
        user_data['username'] = user.username
        user_data['company'] = user.company
        user_data['nik'] = user.nik
        user_data['other_document'] = user.other_document
        user_data['photo'] = user.photo
        output.append(user_data)

    return jsonify({'users': output}), 200

def get_user_by_id(email):
    user = M_User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'No user found!'}), 404

    user_data = {}
    user_data['id'] = user.id
    user_data['email'] = user.email
    user_data['supervisor'] = user.supervisor
    user_data['password'] = user.password
    user_data['created_at'] = user.created_at
    user_data['name'] = user.name
    user_data['username'] = user.username
    user_data['company'] = user.company
    user_data['nik'] = user.nik
    user_data['other_document'] = user.other_document
    user_data['photo'] = user.photo

    return jsonify({'user': user_data}), 200

def delete_user(id):
    user = M_User.query.filter_by(id=id).first()

    if not user:
        return jsonify({'message': 'No user found!'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User has been deleted!'}), 200
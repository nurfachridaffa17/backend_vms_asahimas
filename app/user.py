from .models import db,M_User
from flask import request, jsonify, session
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os
from . import app
import base64

def get_user_folder_path(user_id):
    return os.path.join(app.config['UPLOAD_FOLDER'], str(user_id))

def create_user():
    now = datetime.datetime.now()
    new_user = M_User(
        email = request.form.get('email'),
        password = generate_password_hash(request.form.get('password'), method='scrypt'),
        created_at = now,
        is_active = 1,
        name = request.form.get('name'),
        username = request.form.get('username'),
        company = request.form.get('company'),
        id_usertype = request.form.get('id_usertype'),
        photo = None,
        nik = None,
        other_document = None,
        created_by = session.get('user_id')
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

        if 'photo' in request.files:
            photo = request.files['photo']
            photo.save(os.path.join(user_folder, photo.filename))
            save_photo = user_folder + '/' + photo.filename
            user.photo = save_photo
        
        if 'nik' in request.files:
            nik = request.files['nik']
            nik.save(os.path.join(user_folder, nik.filename))
            save_nik = user_folder + '/' + nik.filename
            user.nik = save_nik
        
        if 'other_document' in request.files:
            other_document = request.files['other_document']
            other_document.save(os.path.join(user_folder, other_document.filename))
            save_other_document = user_folder + '/' + other_document.filename
            user.other_document = save_other_document

            base64_image = base64.b64encode(photo.read())
            user.photo_base64 = base64_image

        db.session.commit()

        return jsonify({'message': 'User updated!'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


def get_all_user():
    users = M_User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['email'] = user.email
        user_data['password'] = user.password
        user_data['created_at'] = user.created_at
        user_data['is_active'] = user.is_active
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
    user_data['password'] = user.password
    user_data['created_at'] = user.created_at
    user_data['is_active'] = user.is_active
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
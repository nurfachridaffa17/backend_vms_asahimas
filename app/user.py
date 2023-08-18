from .models import db,M_User
from flask import request, jsonify
import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import os
from . import app
from flask_login import current_user

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'jpg', 'png', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_user(email, password, username, name, company, nik):
    now = datetime.datetime.now()  
    photo = request.files['photo']
    other_documment = request.files['other_documment']
    updated_by = current_user.id

    if photo and allowed_file(photo.filename):
        file_photo = photo.filename
        user_id = str(uuid.uuid4())
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], user_id, '/photo')
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        photo.save(os.path.join(user_folder, file_photo))
        file_photo = user_folder + '/' + file_photo
    else:
        return jsonify({'message': 'Allowed file type is txt, pdf, jpg, png, jpeg, gif, doc, docx, xls, xlsx'}), 400
    
    if other_documment and allowed_file(other_documment.filename):
        file_doc = other_documment.filename
        user_id = str(uuid.uuid4())
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], user_id, '/other_documment')
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        other_documment.save(os.path.join(user_folder, file_doc))
        file_doc = user_folder + '/' + file_doc
    
    else:
        return jsonify({'message': 'Allowed file type is txt, pdf, jpg, png, jpeg, gif, doc, docx, xls, xlsx'}), 400
    
    new_user = M_User(
        id = 1,
        email = email,
        password = generate_password_hash(password, method='scrypt'),
        created_at = now,
        updated_at = now,
        is_active = 1,
        name = name,
        username = username,
        company = company,
        nik = nik,
        photo = file_photo,
        other_documment = file_doc,
        updated_uid = updated_by,
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'}), 200

def get_all_user():
    users = M_User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['email'] = user.email
        user_data['password'] = user.password
        user_data['created_at'] = user.created_at
        user_data['updated_at'] = user.updated_at
        user_data['is_active'] = user.is_active
        user_data['name'] = user.name
        user_data['username'] = user.username
        user_data['company'] = user.company
        user_data['nik'] = user.nik
        user_data['phone'] = user.phone
        user_data['other_documment'] = user.other_documment
        user_data['photo'] = user.photo
        output.append(user_data)

    return jsonify({'users': output}), 200

def get_user_by_id(id):
    user = M_User.query.filter_by(id=id).first()

    if not user:
        return jsonify({'message': 'No user found!'}), 404

    user_data = {}
    user_data['id'] = user.id
    user_data['email'] = user.email
    user_data['password'] = user.password
    user_data['created_at'] = user.created_at
    user_data['updated_at'] = user.updated_at
    user_data['is_active'] = user.is_active
    user_data['name'] = user.name
    user_data['username'] = user.username
    user_data['company'] = user.company
    user_data['nik'] = user.nik
    user_data['phone'] = user.phone
    user_data['other_documment'] = user.other_documment
    user_data['photo'] = user.photo

    return jsonify({'user': user_data}), 200

def update_user(id):
    user = M_User.query.filter_by(id=id).first()
    data = request.get_json()
    now = datetime.datetime.now()  

    if not user:
        return jsonify({'message': 'No user found!'}), 404

    user.email = data['email']
    user.password = generate_password_hash(data['password'], method='sha256')
    user.updated_at = now
    user.is_active = data['is_active']
    user.name = data['name']
    user.username = data['username']
    user.company = data['company']
    user.nik = data['nik']
    user.phone = data['phone']
    user.other_documment = data['other_documment']
    user.photo = data['photo']

    db.session.commit()

    return jsonify({'message': 'User has been updated!'}), 200

def delete_user(id):
    user = M_User.query.filter_by(id=id).first()

    if not user:
        return jsonify({'message': 'No user found!'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User has been deleted!'}), 200

def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Could not verify', 'WWW-Authenticate': 'Basic realm="Login required!"'}), 401

    user = M_User.query.filter_by(username=auth.username).first()

    if not user:
        return jsonify({'message': 'No user found!'}), 404

    if check_password_hash(user.password, auth.password):
        return jsonify({'message': 'Login success!'}), 200

    return jsonify({'message': 'Login failed!'}), 401
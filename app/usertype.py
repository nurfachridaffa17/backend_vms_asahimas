from .models import db,M_UserType
from flask import request, jsonify
import datetime

def create_usertype():
    now = datetime.datetime.now()
    new_usertype = M_UserType(
        name = request.form.get('name'),
        created_at = now,
        is_active = 1,
    )

    db.session.add(new_usertype)
    db.session.commit()

    return jsonify({'message': 'New usertype created!'}), 200

def get_all_usertype():
    usertypes = M_UserType.query.all()
    if not usertypes:
        return jsonify({'message': 'No usertype found!'}), 404

    output = []
    for usertype in usertypes:
        usertype_data = {}
        usertype_data['id'] = usertype.id
        usertype_data['name'] = usertype.name
        usertype_data['created_at'] = usertype.created_at
        usertype_data['is_active'] = usertype.is_active
        output.append(usertype_data)

    return jsonify({'usertypes': output}), 200

def get_usertype_by_id(id):
    usertype = M_UserType.query.filter_by(id=id).first()
    if not usertype:
        return jsonify({'message': 'No usertype found!'}), 404

    usertype_data = {}
    usertype_data['id'] = usertype.id
    usertype_data['name'] = usertype.name
    usertype_data['created_at'] = usertype.created_at
    usertype_data['is_active'] = usertype.is_active

    return jsonify({'usertype': usertype_data}), 200

def update_usertype(id):
    usertype = M_UserType.query.filter_by(id=id).first()
    if not usertype:
        return jsonify({'message': 'No usertype found!'}), 404
    
    try:
        usertype.name = request.form.get('name')
        usertype.is_active = request.form.get('is_active')
        db.session.commit()
        return jsonify({'message': 'Usertype updated!'}), 200
    except:
        return jsonify({'message': 'Unable to update usertype!'}), 500

def delete_usertype(id):
    usertype = M_UserType.query.filter_by(id=id).first()
    if not usertype:
        return jsonify({'message': 'No usertype found!'}), 404

    db.session.delete(usertype)
    db.session.commit()

    return jsonify({'message': 'Usertype deleted!'}), 200
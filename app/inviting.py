from .models import db, M_Inviting, M_User
from flask import request, jsonify, session
import datetime
from .MailService import send_email
from . import app

status = [
    'Approved',
    'Not Approved'
]

ip = app.config['IP']

def create_inviting():
    email = request.form.get('email'),
    new_inviting = M_Inviting(
        is_active = 1,
        # user_id = user_id,
        email = email,
        access_area_id = request.form.get('access_area_id'),
        # datetime = request.form.get('datetime'),
        purpose = request.form.get('purpose'),
        is_approved = 0,
        status = status[1]
    )

    new_user = M_User(
        email = email,
    )
    try:
        db.session.add(new_inviting)
        db.session.add(new_user)
        db.session.commit()

        test = send_email(
            sender = 'nurfachridaffa17@gmail.com',
            recipients = [email],
            link = ip + '/user?emai={}'.format(email)
            )

        if test:
            return jsonify({'message': 'Inviting created!'}), 201
        else:
            return jsonify({'message': 'Inviting created! But email not sent!'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
def get_all_inviting():
    invitings = M_Inviting.query.all()
    if not invitings:
        return jsonify({'message': 'No inviting found!'}), 404

    output = []
    for inviting in invitings:
        inviting_data = {}
        inviting_data['id'] = inviting.id
        inviting_data['created_by'] = inviting.created_by
        inviting_data['is_active'] = inviting.is_active
        inviting_data['user_id'] = inviting.user_id
        inviting_data['email'] = inviting.email
        inviting_data['access_area_id'] = inviting.access_area_id
        inviting_data['datetime'] = inviting.datetime
        inviting_data['purpose'] = inviting.purpose
        inviting_data['is_approved'] = inviting.is_approved
        inviting_data['approved_by'] = inviting.approved_by
        inviting_data['status'] = inviting.status
        output.append(inviting_data)

    return jsonify({'invitings': output}), 200

def get_inviting_by_id(id):
    inviting = M_Inviting.query.filter_by(id=id).first()
    if not inviting:
        return jsonify({'message': 'No inviting found!'}), 404

    inviting_data = {}
    inviting_data['id'] = inviting.id
    inviting_data['created_by'] = inviting.created_by
    inviting_data['is_active'] = inviting.is_active
    inviting_data['user_id'] = inviting.user_id
    inviting_data['email'] = inviting.email
    inviting_data['access_area_id'] = inviting.access_area_id
    inviting_data['datetime'] = inviting.datetime
    inviting_data['purpose'] = inviting.purpose
    inviting_data['is_approved'] = inviting.is_approved
    inviting_data['approved_by'] = inviting.approved_by
    inviting_data['status'] = inviting.status

    return jsonify({'inviting': inviting_data}), 200


def approved_inviting(id):
    inviting = M_Inviting.query.filter_by(id=id).first()
    if not inviting:
        return jsonify({'message': 'No inviting found!'}), 404

    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'Please login!'}), 401

    inviting.is_approved = 1
    inviting.approved_by = user_id
    inviting.status = status[0]
    try:
        db.session.commit()
        return jsonify({'message': 'Inviting approved!'}), 200
    except:
        return jsonify({'message': 'Inviting not approved!'}), 500


def not_approved_inviting(id):
    inviting = M_Inviting.query.filter_by(id=id).first()
    if not inviting:
        return jsonify({'message': 'No inviting found!'}), 404

    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'Please login!'}), 401

    inviting.is_approved = 0
    inviting.approved_by = user_id
    inviting.status = status[1]
    try:
        db.session.commit()
        return jsonify({'message': 'Inviting not approved!'}), 200
    except:
        return jsonify({'message': 'Inviting not approved!'}), 500


def delete_inviting(id):
    inviting = M_Inviting.query.filter_by(id=id).first()
    if not inviting:
        return jsonify({'message': 'No inviting found!'}), 404
    
    db.session.delete(inviting)
    db.session.commit()

    return jsonify({'message': 'The inviting has been deleted!'}), 200
from .models import db, M_Inviting, M_User, Zkteco, M_Access_Area
from flask import request, jsonify, session
import datetime
from . import app
from flask_mail import Message
from . import mail
import json
import requests

status = [
    'Approved',
    'Rejected',
    'Waiting Approved',
    'Hold'
]

ip = app.config['IP']

def check_user_inviting(email):
    user = M_User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'No user found!'}), 404
    if user.email == email:
        return False
    else:
        return True


def create_inviting():
    email = request.form.get('email')
    domain = request.form.get('domain')
    path = request.form.get('path')
    new_inviting = M_Inviting(
        is_active=1,
        email=email,
        access_area_id=request.form.get('access_area_id'),
        datetime=request.form.get('datetime'),
        purpose=request.form.get('purpose'),
        is_approved=0,
        status=status[2]
    )

    if check_user_inviting(email):
        new_user = M_User(
            email=email,
            id_usertype = 3
        )
        db.session.add(new_user)
    try:
        db.session.add(new_inviting)
        db.session.commit()

        link = domain + path + "?email=" + email

        # Send Email
        msg = Message(
            subject='Selamat Datang di Aplikasi VMS',
            recipients=[email]
        )
        msg.html = '<p>Anda telah diundang oleh PT Asahimas Chemical untuk bergabung di Aplikasi VMS.</p>'
        msg.html += '<p>Silahkan klik link berikut untuk melakukan registrasi.</p>'
        msg.html += '<p><a href="{}">Registrasi</a></p>'.format(link)
        mail.send(msg)

        return jsonify({'message': 'Email sent!'}), 200
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
    data_user = []
    inviting = M_Inviting.query.filter_by(id=id).first()
    get_name = M_User.query.filter_by(email=inviting.email).first()
    # person_photo = get_name.
    if not inviting:
        return jsonify({'message': 'No inviting found!'}), 404

    # user_id = session.get('user_id')
    # if not user_id:
    #     return jsonify({'message': 'Please login!'}), 401

    inviting.is_approved = 1
    # inviting.approved_by = user_id
    inviting.status = status[0]

    url_api = app.config['URL_ENDPOINT'] + '/person/add'
    get_access_area = M_Inviting.query.filter_by(email=inviting.email).order_by(M_Inviting.id.desc()).first()
    area = M_Access_Area.query.filter_by(id=get_access_area.access_area_id).first()
    # if get_access_area.access_area_id == 1:
    #     m_area = M_Access_Area.query.all()
    #     for i in m_area:
    #         area.append(i.access_area_zkteco)
    # else:
    #     m_area = M_Access_Area.query.filter_by(id=get_access_area.access_area_id).first()
    #     area.append(m_area.access_area_zkteco)


    # cookie = Zkteco.query.first()

    headers = {
        'Cookie' : "SESSION=OWUxNDgzZmItYTZlYi00OTYyLTgzZjUtMmQ1N2M1YmUxNzcy",
        'Content-Type' : 'application/json'
    }

    endtime = inviting.datetime + datetime.timedelta(hours=2)

    payload = json.dumps({
        "accEndTime":  str(endtime),
        "accStartTime": str(inviting.datetime),
        "accLevelIds": str(area.access_area_zkteco),
        "deptCode": "1",
        "email": str(get_name.email),
        # "isDisabled": False,
        # "isSendMail": False,
        "name": str(get_name.name),
        # "personPhoto" : None,
        "pin": str(get_name.id)
    })

    try:
        response = requests.requests()
        if response.status_code == 200:
            response_data = response.json()  # Extract JSON data from the response
            
            if response_data["message"] != "success":
                return jsonify({
                    'code': response_data["code"],
                    'message': response_data["message"]
                }), 500
            else:
                return jsonify({
                    'code': response_data["code"],
                    'message': response_data["message"]
                })
        else:
            return jsonify({
                'code': response.status_code,
                'message': response.reason
            }), response.status_code
    except Exception as e:
        return jsonify({'message': str(e)}), 500

    # try:
    #     data = requests.post(url_api, headers=headers, data=payload)
    #     return jsonify({"Message" : data}), 200
        # if data.status_code == 200:
        #     data = data.json()
        #     if data["message"] != "success":
        #         return jsonify({
        #             'code' : data["code"],
        #             'message': data["message"]
        #             }), 500
        #     else:
        #         return jsonify({
        #             'code' : data["code"],
        #             'message': data["message"]
        #         })
    # except Exception as e:
    #     return jsonify({'message': str(e)}), 500 

def hold_inviting(id):
    inviting = M_Inviting.query.filter_by(id=id).first()
    if not inviting:
        return jsonify({'message': 'No inviting found!'}), 404

    # user_id = session.get('user_id')
    # if not user_id:
    #     return jsonify({'message': 'Please login!'}), 401

    inviting.is_approved = 0
    # inviting.approved_by = user_id
    inviting.status = status[3]
    link = 'http://' + ip + "/user?" + inviting.email
    msg = Message(
            subject='UPDATE STATUS REGISTRASI VMS',
            recipients=[inviting.email]
        )
    msg.html = '<p>Anda diminta untuk memperbaiki dokumen untuk kunjungan.</p>'
    msg.html += '<p>Silahkan klik link berikut untuk memperbaiki dokumen.</p>'
    msg.html += '<p><a href="{}">Registrasi</a></p>'.format(link)
    try:
        db.session.commit()
        mail.send(msg)
        return jsonify({'message': 'Invite Was Hold!'}), 200
    except:
        return jsonify({'message': 'Inviting not approved!'}), 500


def not_approved_inviting(id):
    inviting = M_Inviting.query.filter_by(id=id).first()
    if not inviting:
        return jsonify({'message': 'No inviting found!'}), 404

    # user_id = session.get('user_id')
    # if not user_id:
    #     return jsonify({'message': 'Please login!'}), 401

    inviting.is_approved = 0
    # inviting.approved_by = user_id
    inviting.status = status[1]
    msg = Message(
            subject='UPDATE STATUS REGISTRASI VMS',
            recipients=[inviting.email]
        )
    msg.html = '<p>Dokumen kunjungan anda ditolak.</p>'
    msg.html += '<p>Silahkan hubungi PIC anda untuk mengundang kembali dan siapkan dokumen sesuai dengan ketentuan.</p>'
    try:
        db.session.commit()
        mail.send(msg)
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
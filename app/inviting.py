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


def create_inviting(id_user):
    user_id = id_user
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
        status=status[2],
        created_by = user_id
    )

    if check_user_inviting(email):
        new_user = M_User(
            email=email,
            id_usertype = 3,
            supervisor = user_id,
        )
        db.session.add(new_user)
    try:
        db.session.add(new_inviting)
        db.session.commit()

        link = domain + path + "?email=" + email

        # Send Email
        msg = Message(
            sender = "asahimasservice@gmail.com",
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
    inviting_data['email'] = inviting.email
    inviting_data['access_area_id'] = inviting.access_area_id
    inviting_data['datetime'] = inviting.datetime
    inviting_data['purpose'] = inviting.purpose
    inviting_data['is_approved'] = inviting.is_approved
    inviting_data['approved_by'] = inviting.approved_by
    inviting_data['status'] = inviting.status

    return jsonify({'inviting': inviting_data}), 200


def approved_inviting(id, id_user):
    inviting = M_Inviting.query.filter_by(id=id).first()
    get_name = M_User.query.filter_by(email=inviting.email).first()
    if not inviting:
        return jsonify({'message': 'No inviting found!'}), 404

    inviting.is_approved = 1
    inviting.status = status[0]
    inviting.approved_by = id_user

    url_api = app.config['URL_ENDPOINT'] + '/person/add'
    get_access_area = M_Inviting.query.filter_by(email=inviting.email).order_by(M_Inviting.id.desc()).first()

    cookie = Zkteco.query.first()

    headers = {
        'Cookie' : cookie.cookie,
        'Content-Type' : 'application/json'
    }

    endtime = inviting.datetime + datetime.timedelta(hours=2)


    if get_access_area.access_area_id == 1:
        payload = json.dumps({
            "accEndTime" : str(endtime),
            "accStartTime" : str(inviting.datetime),
            "accLevelIds": "4028d8cf8a16edf6018a1b397664002a,4028d8cf89b514e60189b5166a92043a",
            "deptCode": 1,
            "name": get_name.name,
            "personPhoto" : get_name.photo_base64,
            "pin": get_name.id
        })
    else: 
        payload = json.dumps({
            "accEndTime" : str(endtime),
            "accStartTime" : str(inviting.datetime),
            "accLevelIds": "4028d8cf89b514e60189b5166a92043a",
            "deptCode": 1,
            "name": get_name.name,
            "personPhoto" : str(get_name.photo_base64),
            "pin": get_name.id
        })

    try:
        data = requests.post(url_api, headers=headers, data=payload)
        if data.status_code == 200:
            data = data.json()
            if data["message"] != "success":
                return jsonify({'code' : data["code"],'message': data["message"]}), 500
            else:
                db.session.commit()
                msg_vst = Message(
                    sender = "asahimasservice@gmail.com",
                    subject='STATUS REGISTRASI VMS - DISETUJUI',
                    recipients=[inviting.email]
                    )
                datetime_str = str(inviting.datetime)
                datetime_obj = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
                msg_vst.html = '<p>Undangan anda disetujui.</p>'
                msg_vst.html += '<p>Silahkan berkunjung pada waktu yang telah ditentukan.</p>'
                msg_vst.html += '<p>Waktu Kunjungan : {}</p>'.format(datetime_obj)

                id_inviter = inviting.created_by
                get_inviter = M_User.query.filter_by(id=id_inviter).first()
                email_inviter = get_inviter.email

                id_supervisor = M_User.query.filter_by(id=get_inviter.supervisor).first()
                email_supervisor = id_supervisor.email

                msg_inviter = Message(
                    sender = "asahimasservice@gmail.com",
                    subject='STATUS REGISTRASI VMS - DISETUJUI',
                    recipients=[email_inviter],
                    cc = [email_supervisor]
                )
                # datetime_obj = datetime.datetime.strptime(inviting.datetime, "%d%b%Y%H%M%S")
                msg_vst.html = '<p>Tamu bernama {} akan berkunjung menemui {}.</p>'.format(get_name.name, get_inviter.name)
                msg_vst.html += '<p>Waktu Kunjungan : {}</p>'.format(datetime_obj)

                mail.send(msg_vst)
                mail.send(msg_inviter)

                return jsonify({'code' : data["code"],'message': data["message"]}), 200

        else:
            return jsonify({
                'code': data.status_code,
            }), data.status_code
    except Exception as e:
        return jsonify({'message': str(e)}), 500 

def hold_inviting(id, id_user):
    inviting = M_Inviting.query.filter_by(id=id).first()
    get_name = M_User.query.filter_by(email=inviting.email).first()
    if not inviting:
        return jsonify({'message': 'No inviting found!'}), 404

    inviting.is_approved = 0
    inviting.approved_by = id_user
    inviting.status = status[3]
    link = 'http://' + ip + "/user?" + inviting.email
    msg_vst = Message(
        sender = "asahimasservice@gmail.com",
        subject='UPDATE STATUS REGISTRASI VMS - REVISI',
        recipients=[inviting.email]
        )
    msg_vst.html = '<p>Anda diminta untuk memperbaiki dokumen untuk kunjungan.</p>'
    msg_vst.html += '<p>Silahkan klik link berikut untuk memperbaiki dokumen.</p>'
    msg_vst.html += '<p><a href="{}">Registrasi</a></p>'.format(link)

    id_inviter = inviting.created_by
    get_inviter = M_User.query.filter_by(id=id_inviter).first()
    email_inviter = get_inviter.email

    id_supervisor = M_User.query.filter_by(id=get_inviter.supervisor).first()
    email_supervisor = id_supervisor.email

    # return jsonify({'message' : str(user_spv)}), 200

    msg_inviter = Message(
        sender = "asahimasservice@gmail.com",
        subject='STATUS REGISTRASI VMS - REVISI',
        recipients=[email_inviter],
        cc = [email_supervisor]
    )
    msg_inviter.html = '<p>Tamu bernama {} perlu melakukan revisi dokumen.</p>'.format(get_name.name)
    try:
        db.session.commit()
        mail.send(msg_vst)
        mail.send(msg_inviter)
        return jsonify({'message': 'Invite Was Hold!'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


def not_approved_inviting(id, id_user):
    inviting = M_Inviting.query.filter_by(id=id).first()
    get_name = M_User.query.filter_by(email=inviting.email).first()
    if not inviting:
        return jsonify({'message': 'No inviting found!'}), 404

    inviting.is_approved = 0
    inviting.approved_by = id_user
    inviting.status = status[1]
    msg = Message(
        sender = "asahimasservice@gmail.com",
        subject='UPDATE STATUS REGISTRASI VMS - DITOLAK',
        recipients=[inviting.email]
    )
    msg.html = '<p>Dokumen kunjungan anda ditolak.</p>'
    msg.html += '<p>Silahkan hubungi PIC anda untuk mengundang kembali dan siapkan dokumen sesuai dengan ketentuan.</p>'

    id_inviter = inviting.created_by
    get_inviter = M_User.query.filter_by(id=id_inviter).first()
    email_inviter = get_inviter.email

    id_supervisor = M_User.query.filter_by(id=get_inviter.supervisor).first()
    email_supervisor = id_supervisor.email

    msg_inviter = Message(
        subject='STATUS REGISTRASI VMS - DITOLAK',
        recipients=[email_inviter],
        cc = [email_supervisor]
    )
    msg_inviter.html = '<p>Undangan anda untuk {} telah ditolak silakan kirim undangan kembali.</p>'.format(get_name.name, get_inviter.name)

    try:
        db.session.commit()
        mail.send(msg)
        mail.send(msg_inviter)
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
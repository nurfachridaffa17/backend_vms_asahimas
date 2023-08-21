from flask_mail import Message
from .models import db
from . import mail
from flask import jsonify, request
from .log_service import LoggingService
from . import app

logging_service = LoggingService(app)


def send_email(link):
    msg = Message(
        subject='Selamat Datang di Aplikasi VMS-SERELO',
        recipients=request.form.get('email')
    )
    link = request.form.get('link')
    msg.html = '<p>Anda telah diundang oleh PT.ASAHIMAS untuk bergabung di Aplikasi VMS-SERELO</p>'
    msg.html += '<p>Silahkan klik link berikut untuk melakukan registrasi</p>'
    msg.html += '<p><a href="{}">Registrasi</a></p>'.format(link)

    # try:
    #     mail.send(msg)
    #     logging_service.log_info('Email sent!')
    #     return jsonify({'message': 'Email sent successfully'}), 200
    # except Exception as e:
    #     logging_service.log_error(str(e))
    #     return jsonify({'message': 'Email sending failed'}), 400
    
    try:
        mail.send(msg)
        return jsonify({'message': 'Email sent!'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

def send_email_accepted(sender, recipients, acceptor, access_area, tanggal, user, company, purpose, employee):
    msg = Message(
        subject='Selamat Datang di Aplikasi VMS-SERELO',
        sender=sender,
        recipients=recipients
    )
    msg.html = '<p>Kepada {}</p>'.format(acceptor)
    msg.html += '<p>Kami menginformasikan bahwa registrasi Anda untuk akses ke area {} pada tanggal {} telah Berhasil Disetujui. Berikut rincian informasi registrasi Anda</p>'.format(access_area, tanggal)
    msg.html += '<ul> <li>Username : {}</li> <li>Perusahaan : {}</li> <li>Area Akses : {}</li> <li>Tanggal Dan Waktu : {} </li> <li>Tujuan : {} </li> </ul>'.format(user, company, access_area, tanggal, purpose)
    msg.html += '<p>Terima Kasih</p>'
    msg.html += '<p>Salam</p>'
    msg.html += '<p>{}</p>'.format(employee)

    try:
        mail.send(msg)
        return jsonify({'message': 'Email sent!'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

def send_email_rejected(sender, recipients, acceptor, access_area, tanggal, link):
    msg = Message(
        subject='Selamat Datang di Aplikasi VMS-SERELO',
        sender=sender,
        recipients=recipients
    )
    msg.html = '<p>Kepada {}</p>'.format(acceptor)
    msg.html += '<p>Kami menginformasikan bahwa registrasi Anda untuk akses ke area {} pada tanggal {} telah Gagal'.format(access_area, tanggal)
    msg.html += '<p>Pengunjung harap memperbaiki data diri melalui link berikut ini</p>'
    msg.html += '<p><a href="{}">Registrasi</a></p>'.format(link)
    msg.html += '<p>Terima Kasih</p>'

    try:
        mail.send(msg)
        return jsonify({'message': 'Email sent!'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


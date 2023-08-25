from .models import db,Zkteco
from flask import request, jsonify, session
import datetime

def update_cookies(id):
    cookie_id = Zkteco.query.filter_by(id=id).first()

    if not cookie_id:
        return jsonify({'message': 'No cookies found!'}), 404
    
    try:
        cookie = request.form.get('cookie')
        cookie_id.cookie = cookie
        db.session.commit()
        return jsonify({'message': 'Cookies updated!'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

def get_all_cookies():
    cookies = Zkteco.query.all()
    output = []
    for cookie in cookies:
        cookie_data = {}
        cookie_data['id'] = cookie.id
        cookie_data['cookie'] = cookie.cookie
        output.append(cookie_data)

    return jsonify({'cookies': output}), 200

def get_cookies_by_id(id):
    cookie = Zkteco.query.filter_by(id=id).first()

    if not cookie:
        return jsonify({'message': 'No cookies found!'}), 404

    cookie_data = {}
    cookie_data['id'] = cookie.id
    cookie_data['cookie'] = cookie.cookie

    return jsonify({'cookie': cookie_data}), 200
    

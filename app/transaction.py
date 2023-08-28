from .models import db,M_User,M_UserType,M_Access_Area,M_Card, T_Rfid,M_Inviting,Zkteco
from flask import request, jsonify
import datetime
import random
from . import app
import json
import requests
from .log_file import LogFile

log = LogFile('transaction')

def create_transaction():
    card_id = request.form.get('card_id')
    user_id = request.form.get('user_id')

    get_zkteco = Zkteco.query.first()

    url = str(get_zkteco.ip) + "/person/addPersonnelBasicInfo"

    check_card = M_Card.query.filter_by(id=card_id).first()
    if check_card.is_used == 1:
        return jsonify({'message': 'Card is used!'}), 404
    
    payload = json.dumps({
        "cardNo" : str(check_card.card_number),
        "pin": user_id
    })

    headers = {
        'Cookie' : get_zkteco.cookie,
        'Content-Type' : 'application/json'
    }
    try:
        data = requests.post(url, headers=headers, data=payload)
        if data.status_code == 200:
            data = data.json()
            if data["message"] != "success":
                log.log.warning("code" + data["code"] + "message" + data["message"])
                return jsonify({
                    'code' : data["code"],
                    'message': data["message"]
                    }), 500
            else:
                new_transaction = T_Rfid(
                    card_id = card_id,
                    user_id = user_id,
                    is_active = 1,
                    check_in = datetime.datetime.now(),
                )

                check_card.is_used = 1
                db.session.add(new_transaction)
                db.session.commit()

                log.log.info('New transaction created! ' + str(new_transaction.id))
                return jsonify({
                    'code' : data["code"],
                    'message': data["message"],
                    'id' : new_transaction.id
                }), 200

        else:
            log.log.warning("code" + data["code"] + "message" + data["message"])
            return jsonify({
                'code': data.status_code,
            }), data.status_code
    except Exception as e:
        log.log.error(str(e))
        return jsonify({'message': 'there is problem for created transaction'}), 500
    
def get_all_transaction():
    transactions = T_Rfid.query.all()
    if not transactions:
        return jsonify({'message': 'No transaction found!'}), 404

    output = []
    for transaction in transactions:
        transaction_data = {}
        transaction_data['id'] = transaction.id
        transaction_data['card_id'] = transaction.card_id
        transaction_data['user_id'] = transaction.user_id
        transaction_data['is_active'] = transaction.is_active
        transaction_data['check_in'] = transaction.check_in
        transaction_data['check_out'] = transaction.check_out
        output.append(transaction_data)

    return jsonify({'transactions': output}), 200

def transaction_check_out(id):
    transaction = T_Rfid.query.filter_by(id=id).first()
    card_id = transaction.card_id
    if not transaction:
        return jsonify({'message': 'No transaction found!'}), 404

    check_card = M_Card.query.filter_by(id=card_id).first()
    check_card.is_used = 0

    transaction.check_out = datetime.datetime.now()
    transaction.is_active = 0
    db.session.commit()

    return jsonify({'message': 'Transaction check out success!'}), 200

def get_transaction_by_id(id):
    transaction = T_Rfid.query.filter_by(id=id).first()
    if not transaction:
        return jsonify({'message': 'No transaction found!'}), 404

    transaction_data = {}
    transaction_data['id'] = transaction.id
    transaction_data['card_id'] = transaction.card_id
    transaction_data['name'] = transaction.name
    transaction_data['is_active'] = transaction.is_active
    transaction_data['check_in'] = transaction.check_in
    transaction_data['check_out'] = transaction.check_out

    return jsonify({'transaction': transaction_data}), 200

def delete_transaction(id):
    transaction = T_Rfid.query.filter_by(id=id).first()
    if not transaction:
        return jsonify({'message': 'No transaction found!'}), 404

    db.session.delete(transaction)
    db.session.commit()

    return jsonify({'message': 'Transaction deleted!'}), 200






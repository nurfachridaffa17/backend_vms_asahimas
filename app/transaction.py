from .models import db, M_User, M_UserType, M_Access_Area, M_Card, T_Rfid, M_Inviting
from flask import request, jsonify
import datetime
import random

def create_transaction():
    card_id = request.form.get('card_id')
    user_id = request.form.get('user_id')
    check_card = M_Card.query.filter_by(id=card_id).first()
    if check_card.is_used == 1:
        return jsonify({'message': 'Card is used!'}), 404
    
    try:
        new_transaction = T_Rfid(
            card_id = card_id,
            user_id = user_id,
            is_active = 1,
            check_in = datetime.datetime.now(),
        )

        check_card.is_used = 1

        db.session.add(new_transaction)
        db.session.commit()
        return jsonify({'message': 'Change card is success!'}), 200
    except:
        return jsonify({'message': 'Change card is failed!'}), 404
    
def get_all_transaction():
    transactions = T_Rfid.query.all()
    if not transactions:
        return jsonify({'message': 'No transaction found!'}), 404

    output = []
    for transaction in transactions:
        transaction_data = {}
        transaction_data['id'] = transaction.id
        transaction_data['card_id'] = transaction.card_id
        transaction_data['name'] = transaction.name
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






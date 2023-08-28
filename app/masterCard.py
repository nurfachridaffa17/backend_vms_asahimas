from .models import db,M_Card
from flask import request, jsonify
import datetime
import os
from . import app
from .log_file import LogFile

log = LogFile('card')

def create_card():
    now = datetime.datetime.now()  
    new_card = M_Card(
        card_number = request.form.get('card_number'),
        name = request.form.get('name'),
        created_at = now,
        is_active = 1,
        is_used = 0,
    )
    try:
        db.session.add(new_card)
        db.session.commit()

        log.log.info('New card created! ' + str(new_card.card_number))
        return jsonify({'message': 'New card created!'}), 200
    except Exception as e:
        log.log.error(str(e))
        return jsonify({'message': 'there is problem with created card'}), 500

def get_all_card():
    cards = M_Card.query.all()
    if not cards:
        return jsonify({'message': 'No card found!'}), 404

    output = []
    for card in cards:
        card_data = {}
        card_data['id'] = card.id
        card_data['card_number'] = card.card_number
        card_data['name'] = card.name
        card_data['created_at'] = card.created_at
        card_data['is_active'] = card.is_active
        card_data['is_used'] = card.is_used
        output.append(card_data)

    return jsonify({'cards': output}), 200

def get_card_by_id(id):
    card = M_Card.query.filter_by(id=id).first()
    if not card:
        return jsonify({'message': 'No card found!'}), 404

    card_data = {}
    card_data['id'] = card.id
    card_data['card_number'] = card.card_number
    card_data['name'] = card.name
    card_data['created_at'] = card.created_at
    card_data['is_active'] = card.is_active
    card_data['is_used'] = card.is_used

    return jsonify({'card': card_data}), 200

def get_card_not_use():
    unused_cards = M_Card.query.filter_by(is_used=0).all()

    if not unused_cards:
        return jsonify({'message': 'No unused cards found!'}), 404

    cards_data = []
    for card in unused_cards:
        card_data = {
            'id': card.id,
            'card_number': card.card_number,
            'name': card.name,
            'created_at': card.created_at,
            'is_active': card.is_active,
            'is_used': card.is_used
        }
        cards_data.append(card_data)

    return jsonify({'cards': cards_data}), 200

def update_card(id):
    card = M_Card.query.filter_by(id=id).first()
    if not card:
        return jsonify({'message': 'No card found!'}), 404
    
    try:
        card.card_number = request.form.get('card_number')
        card.name = request.form.get('name')
        card.is_active = request.form.get('is_active')
        card.is_used = request.form.get('is_used')
        db.session.commit()

        log.log.info('Card updated! ' + str(card.card_number) + ' ' + str(card.id))
        return jsonify({'message': 'Card updated!'}), 200
    except Exception as e:
        log.log.error(str(e))
        return jsonify({'message': 'Failed to update card!'}), 400

def delete_card(id):
    card = M_Card.query.filter_by(id=id).first()
    if not card:
        return jsonify({'message': 'No card found!'}), 404

    db.session.delete(card)
    db.session.commit()

    return jsonify({'message': 'Card has been deleted!'}), 200
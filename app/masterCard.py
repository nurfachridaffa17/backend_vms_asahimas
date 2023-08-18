from .models import db,M_Card
from flask import request, jsonify
import datetime
import os
from . import app

def create_card():
    now = datetime.datetime.now()  
    new_card = M_Card(
        card_number = request.form.get('card_number'),
        name = request.form.get('name'),
        created_at = now,
        is_active = 1,
    )

    db.session.add(new_card)
    db.session.commit()

    return jsonify({'message': 'New card created!'}), 200

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

    return jsonify({'card': card_data}), 200

def update_card(id):
    card = M_Card.query.filter_by(id=id).first()
    if not card:
        return jsonify({'message': 'No card found!'}), 404
    
    try:
        card.card_number = request.form.get('card_number')
        card.name = request.form.get('name')
        db.session.commit()
    except:
        return jsonify({'message': 'Failed to update card!'}), 400

    return jsonify({'message': 'Card updated!'}), 200

def delete_card(id):
    card = M_Card.query.filter_by(id=id).first()
    if not card:
        return jsonify({'message': 'No card found!'}), 404

    db.session.delete(card)
    db.session.commit()

    return jsonify({'message': 'Card has been deleted!'}), 200
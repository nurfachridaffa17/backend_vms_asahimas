from .models import db,M_Access_Area
from flask import request, jsonify
import datetime

def create_access_area():
    new_access_area = M_Access_Area(
        name = request.form.get('name'),
        is_active = 1,
    )

    db.session.add(new_access_area)
    db.session.commit()

    return jsonify({'message': 'New access area created!'}), 200

def get_all_access_area():
    access_areas = M_Access_Area.query.all()
    if not access_areas:
        return jsonify({'message': 'No access area found!'}), 404

    output = []
    for access_area in access_areas:
        access_area_data = {}
        access_area_data['id'] = access_area.id
        access_area_data['name'] = access_area.name
        access_area_data['is_active'] = access_area.is_active
        output.append(access_area_data)

    return jsonify({'access_areas': output}), 200

def get_access_area_by_id(id):
    access_area = M_Access_Area.query.filter_by(id=id).first()
    if not access_area:
        return jsonify({'message': 'No access area found!'}), 404

    access_area_data = {}
    access_area_data['id'] = access_area.id
    access_area_data['name'] = access_area.name
    access_area_data['is_active'] = access_area.is_active

    return jsonify({'access_area': access_area_data}), 200

def update_access_area(id):
    access_area = M_Access_Area.query.filter_by(id=id).first()
    if not access_area:
        return jsonify({'message': 'No access area found!'}), 404
    
    try:
        access_area.name = request.form.get('name')
        access_area.is_active = request.form.get('is_active')
        db.session.commit()
        return jsonify({'message': 'Access area updated!'}), 200
    except:
        return jsonify({'message': 'Access area not updated!'}), 500

def delete_access_area(id):
    access_area = M_Access_Area.query.filter_by(id=id).first()
    if not access_area:
        return jsonify({'message': 'No access area found!'}), 404

    db.session.delete(access_area)
    db.session.commit()

    return jsonify({'message': 'Access area deleted!'}), 200
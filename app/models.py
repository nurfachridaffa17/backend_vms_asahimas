from . import db

class M_User(db.Model):
    __tablename__ = 'm_user'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime)
    is_active = db.Column(db.Integer)
    id_usertype = db.Column(db.Integer)
    name = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))
    company = db.Column(db.String(255))
    nik = db.Column(db.String(255))
    other_document = db.Column(db.String(255))
    photo = db.Column(db.String(255))

    def __repr__(self):
        return '<M_User {}>'.format(self.name)
    
    def serialize(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'is_active': self.is_active,
            'id_usertype': self.id_usertype,
            'name': self.name,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'company': self.company,
            'nik': self.nik,
            'other_document': self.other_document,
            'photo': self.photo,
        }

class M_UserType(db.Model):
    __tablename__ = 'm_usertype'
    id = db.Column(db.Integer, primary_key=True)
    created_uid = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_uid = db.Column(db.Integer)
    updated_at = db.Column(db.DateTime)
    is_active = db.Column(db.Integer)
    name = db.Column(db.String(255))

    def __repr__(self):
        return '<M_UserType {}>'.format(self.name)
    
    def serialize(self):
        return {
            'id': self.id, 
            'created_at': self.created_at,
            'updated_uid': self.updated_uid,
            'updated_at': self.updated_at,
            'is_active': self.is_active,
            'name': self.name,
            'created_uid': self.created_uid,
        }

class M_Card(db.Model):
    __tablename__ = 'm_card'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime)
    card_number = db.Column(db.String(255))
    name = db.Column(db.String(255))
    is_used = db.Column(db.Integer)
    is_active = db.Column(db.Integer)
    
    def __repr__(self):
        return '<M_Card {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id, 
            'created_at': self.created_at,
            'card_number': self.card_number,
            'name': self.name,
            'is_used': self.is_used,
            'is_active' : self.is_active,
        }

class M_Inviting(db.Model):
    __tablename__ = 'm_inviting'
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer)
    is_active = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    email = db.Column(db.String(255))
    access_area_id = db.Column(db.Integer)
    datetime = db.Column(db.DateTime)
    purpose = db.Column(db.String(255))
    is_approved = db.Column(db.Integer)
    approved_by = db.Column(db.Integer)
    status = db.Column(db.Integer)

    def __repr__(self):
        return '<M_Inviting {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'created_by': self.created_by,
            'is_active': self.is_active,
            'user_id': self.user_id,
            'email': self.email,
            'access_area_id': self.access_area_id,
            'datetime': self.datetime,
            'purpose': self.purpose,
        }

class M_Access_Area(db.Model):
    __tablename__ = 'm_accessarea'
    id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Integer)
    name = db.Column(db.String(255))

    def __repr__(self):
        return '<M_Access_Area {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id, 
            'is_active': self.is_active,
            'name': self.name,
        }


class T_Rfid(db.Model):
    __tablename__ = 't_rfid'
    id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Integer)
    name = db.Column(db.String(255))
    card_id = db.Column(db.Integer)
    check_in = db.Column(db.DateTime)
    check_out = db.Column(db.DateTime)

    def __repr__(self):
        return '<T_Rfid {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id, 
            'is_active': self.is_active,
            'name': self.name,
            'card_id': self.card_id,
            'check_in': self.check_in,
            'check_out': self.check_out,
        }


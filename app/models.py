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
    created_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer)
    updated_at = db.Column(db.DateTime)

    def __init__(self, created_at, updated_by, updated_at, created_by):
        self.created_by = created_by
        self.created_at = created_at
        self.updated_by = updated_by
        self.updated_at = updated_at
    
    def __repr__(self):
        return '<M_Card {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id, 
            'created_at': self.created_at,
            'updated_by': self.updated_by,
            'updated_at': self.updated_at,
            'created_by': self.created_by,
        }
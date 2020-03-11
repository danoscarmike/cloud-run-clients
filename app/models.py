from app import db
from app.enums import ProtoSourceEnum

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    events = db.relationship('Event', backref='creator', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username} {self.id}>'

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    proto_url = db.Column(db.String(128))
    proto_url_type = db.Column(db.Enum(ProtoSourceEnum))

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, index=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    success = db.Column(db.Boolean)
    google_api = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Event {self.id}/{self.created}>'

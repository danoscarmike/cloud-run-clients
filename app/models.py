from app import db, login
from app.enums import ProtoSourceEnum
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    events = db.relationship('Event', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username} {self.id}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    title = db.Column(db.String(128))
    version = db.Column(db.String(64))
    proto_url = db.Column(db.String(128))
    proto_source = db.Column(db.Enum(ProtoSourceEnum))
    is_google_api = db.Column(db.Boolean)
    updated = db.Column(db.DateTime, index=True)
    events = db.relationship('Event', backref='service', lazy='dynamic')

    def __repr__(self):
        return f'<Service {self.name}:{self.version}>'

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, index=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    success = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Event {self.id}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
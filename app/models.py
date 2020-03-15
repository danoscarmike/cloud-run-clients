from app import db, login
from app.enums import ProtoSourceEnum
from datetime import datetime
from flask_login import UserMixin
from hashlib import md5
from werkzeug.security import check_password_hash, generate_password_hash


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_service_id', db.Integer, db.ForeignKey('service.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    events = db.relationship('Event', backref='user', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    services_followed = db.relationship(
        'Service',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def __repr__(self):
        return f'<User {self.username} {self.id}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=robohash&s={size}'

    def is_following(self, service):
        return self.services_followed.filter(
            followers.c.followed_service_id == service.id).count() > 0

    def follow(self, service):
        if not self.is_following(service):
            self.followed.append(service)

    def unfollow(self, service):
        if self.is_following(service):
            self.followed.remove(service)

    def followed_events(self):
        return Event.query.join(
            followers, (followers.c.followed_service_id ==
                        Event.service_id)).filter(
                followers.c.follower_id == self.id).order_by(
                    Event.created.desc())


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
    user_followers = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.followed_service_id == id),
        backref=db.backref('followed', lazy='dynamic'),
        lazy='dynamic'
    )

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

    def format_datetime(self, created):
        return self.created.strftime("%A, %b %d, %Y %t %Z")


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

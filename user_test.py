from app import app, db
from app.models import User, Service, Event
from datetime import datetime, timedelta


class TestUserModel:
    @classmethod
    def setup_class(cls):
        app.config['SQLALLCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()
        u1 = User(username='oscar')
        u2 = User(username='bigbird', email='bb@sesame.street')
        u3 = User(username='ernie', email='ern@bande.com')
        s1 = Service(name='vision', version='v1', updated=datetime.utcnow())
        s2 = Service(name='translate', version='v3', updated=datetime.utcnow())
        db.session.add_all([u1, u2, u3, s1, s2])
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User.query.filter_by(username='oscar').first()
        u.set_password('garbage')
        assert not u.check_password('gold')
        assert u.check_password('garbage')

    def test_avatar(self):
        u = User.query.filter_by(username='bigbird').first()
        assert u.avatar(64) == 'https://www.gravatar.com/avatar/' \
                               '20e1af6ab5d496cc7ba3827acae7196e' \
                               '?d=robohash&s=64'

    def test_follow(self):
        u1 = User.query.filter_by(username='oscar').first()
        s1 = Service.query.filter_by(name='vision').first()
        assert u1.services_followed.all() == []

        u1.follow(s1)
        db.session.commit()
        assert u1.is_following(s1)
        assert u1.services_followed.count() == 1
        assert u1.services_followed.first().name == 'vision'
        assert s1.user_followers.count() == 1
        assert s1.followers.first().username == 'oscar'

        u1.unfollow(s1)
        db.session.commit()
        assert not u1.is_following(s1)
        assert u1.services_followed.count() == 0
        assert s1.user_followers.count() == 0

    def test_followed_events(self):
        u1 = User.query.filter_by(username='oscar').first()
        u2 = User.query.filter_by(username='bigbird').first()
        u3 = User.query.filter_by(username='ernie').first()
        s1 = Service.query.filter_by(name='vision').first()
        s2 = Service.query.filter_by(name='translate').first()

        e1 = Event(
            created=datetime.utcnow() + timedelta(seconds=3),
            service_id=1,
            user_id=1
        )
        e2 = Event(
            created=datetime.utcnow() + timedelta(seconds=2),
            service_id=1,
            user_id=2
        )
        e3 = Event(
            created=datetime.utcnow() + timedelta(seconds=1),
            service_id=2,
            user_id=3
        )
        db.session.add_all([e1, e2, e3])
        db.session.commit()

        u1.follow(s1)
        u2.follow(s2)
        u3.follow(s1)
        u3.follow(s2)
        db.session.commit()

        f1 = u1.followed_events().all()
        f2 = u2.followed_events().all()
        f3 = u3.followed_events().all()

        assert f1 == [e1, e2]
        assert f2 == [e3]
        assert f3 == [e1, e2, e3]

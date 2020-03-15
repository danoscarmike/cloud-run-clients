import unittest
from app import app, db
from app.models import User, Service, Event
from datetime import datetime, timedelta


class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALLCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='oscar')
        u.set_password('garbage')
        self.assertFalse(u.check_password('gold'))
        self.assertTrue(u.check_password('garbage'))

    def test_avatar(self):
        u = User(username='bigbird', email='bb@sesame.street')
        self.assertEqual(u.avatar(64), ('https://www.gravatar.com/avatar/'
                                        '20e1af6ab5d496cc7ba3827acae7196e?'
                                        'd=robohash&s=64'))

    def test_follow(self):
        u1 = User(username='oscar', email='oscar@garbagecan.com')
        s1 = Service(name='vision', version='v1', updated=datetime.utcnow())
        db.session.add_all([u1, s1])
        db.session.commit()
        self.assertEqual(u1.services_followed.all(), [])

        u1.follow(s1)
        db.session.commit()
        self.assertTrue(u1.is_following(s1))
        self.assertEqual(u1.services_followed.count(), 1)
        self.assertEqual(u1.services_followed.first().name, 'vision')
        self.assertEqual(s1.user_followers.count(), 1)
        self.assertEqual(s1.followers.first().username, 'oscar')

        u1.unfollow(s1)
        db.session.commit()
        self.assertFalse(u1.is_following(s1))
        self.assertEqual(u1.services_followed.count(), 0)
        self.assertEqual(s1.user_followers.count(), 0)

    def test_followed_events(self):
        u1 = User(username='oscar', email='oscar@garbagecan.com')
        u2 = User(username='bigbird', email='bb@sesame.street')
        u3 = User(username='ernie', email='ern@bande.com')
        s1 = Service(name='vision', version='v1', updated=datetime.utcnow())
        s2 = Service(name='translate', version='v3', updated=datetime.utcnow())
        db.session.add_all([u1, u2, u3, s1, s2])

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
        self.assertEqual(f1, [e1, e2])
        self.assertEqual(f2, [e3])
        self.assertEqual(f3, [e1, e2, e3])


if __name__ == '__main__':
    unittest.main(verbosity=2)

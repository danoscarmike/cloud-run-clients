from app import db
from app.enums import ProtoSourceEnum
from app.models import User, Service, Event
from datetime import datetime as dt


dan = User(
    username='danoscarmike',
    email='omeara.dan@gmail.com',
    first_name='Dan',
    last_name='O\'Meara'
)
dan.set_password('abc123')
monkey = User(
    username='testmonkey',
    email='monkey@test.com',
    first_name='Test',
    last_name='Monkey'
)
monkey.set_password('abc123')

vision = Service(
    name='vision',
    title='Cloud Vision API',
    version='v1',
    proto_url='https://github.com/googleapis/\
        googleapis/tree/master/google/cloud/vision/v1',
    proto_source=ProtoSourceEnum.googleapis,
    is_google_api=True,
    updated=dt.now()
)

translate = Service(
    name='translate',
    title='Cloud Translation API',
    version='v3',
    proto_url='https://github.com/googleapis/\
        googleapis/tree/master/google/cloud/translate/v3',
    proto_source=ProtoSourceEnum.googleapis,
    is_google_api=True,
    updated=dt.now()
)

db.session.add(dan)
db.session.add(monkey)
db.session.add(vision)
db.session.add(translate)

dan_event1 = Event(
    created=dt.now(),
    service_id=Service.query.filter_by(name='vision').first().id,
    success=True,
    user_id=User.query.filter_by(username='danoscarmike').first().id
)

db.session.add(dan_event1)

db.session.commit()

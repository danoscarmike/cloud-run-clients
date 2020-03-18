import pytz

from app import db
from app.enums import ProtoSourceEnum
from app.models import User, Service, Event
from connectors.google_apis import get_api_details, list_apis, list_api_versions
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
gorilla = User(
    username='qualitygorilla',
    email='gorilla@quality.com',
    first_name='Quality',
    last_name='Gorilla'
)
gorilla.set_password('abc123')

vision = Service(
    name='vision',
    title='Cloud Vision API',
    version='v1',
    proto_url='https://github.com/googleapis/'
              'googleapis/tree/master/google/cloud/vision/v1',
    proto_source=ProtoSourceEnum.googleapis,
    is_google_api=True,
    updated=pytz.utc.localize(dt.utcnow())
)

translate = Service(
    name='translate',
    title='Cloud Translation API',
    version='v3',
    proto_url='https://github.com/googleapis/'
              'googleapis/tree/master/google/cloud/translate/v3',
    proto_source=ProtoSourceEnum.googleapis,
    is_google_api=True,
    updated=pytz.utc.localize(dt.utcnow())
)

language = Service(
    name='language',
    title='Cloud Natural Language API',
    version='v3',
    proto_url='https://github.com/googleapis/'
              'googleapis/tree/master/google/cloud/language/v1',
    proto_source=ProtoSourceEnum.googleapis,
    is_google_api=True,
    updated=pytz.utc.localize(dt.utcnow())
)

for api in list_apis():
    for version in list_api_versions(api):
        if Service.query.filter_by(name=api, version=version).first() is None:
            title, summary = get_api_details(api, version)
            new_service = Service(
                name=api,
                version=version,
                title=title,
                summary=summary,
                proto_source=ProtoSourceEnum.googleapis,
                is_google_api=True,
                updated=pytz.utc.localize(dt.utcnow())
            )
            db.session.add(new_service)


db.session.add(dan)
db.session.add(monkey)
db.session.add(gorilla)
# db.session.add(vision)
# db.session.add(translate)
# db.session.add(language)

dan_event1 = Event(
    created=pytz.utc.localize(dt.utcnow()),
    service_id=Service.query.filter_by(name='vision').first().id,
    success=True,
    user_id=User.query.filter_by(username='danoscarmike').first().id
)

dan_event2 = Event(
    created=pytz.utc.localize(dt.utcnow()),
    service_id=Service.query.filter_by(name='translate').first().id,
    success=False,
    user_id=User.query.filter_by(username='danoscarmike').first().id
)

monkey_event1 = Event(
    created=pytz.utc.localize(dt.utcnow()),
    service_id=Service.query.filter_by(name='translate').first().id,
    success=True,
    user_id=User.query.filter_by(username='testmonkey').first().id
)

monkey_event2 = Event(
    created=pytz.utc.localize(dt.utcnow()),
    service_id=Service.query.filter_by(name='language').first().id,
    success=True,
    user_id=User.query.filter_by(username='testmonkey').first().id
)

gorilla_event1 = Event(
    created=pytz.utc.localize(dt.utcnow()),
    service_id=Service.query.filter_by(name='vision').first().id,
    success=True,
    user_id=User.query.filter_by(username='qualitygorilla').first().id
)

db.session.add(dan_event1)
db.session.add(dan_event2)
db.session.add(monkey_event1)
db.session.add(monkey_event2)
db.session.add(gorilla_event1)

db.session.commit()

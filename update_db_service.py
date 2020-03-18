from app import db
from app.models import Service
from connectors.google_apis import get_api_details, list_apis

for api in list_apis():
    service_versions = Service.query.filter_by(name=api).all()
    for service in service_versions:
        if service.title is None:
            service.title, service.summary = get_api_details(api, service.version)
            db.session.add(service)
            db.session.commit()


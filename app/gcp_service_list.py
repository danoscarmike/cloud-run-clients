import os

from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
SERVICE_ACCOUNT_FILE = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

credentials = service_account.Credentials.from_service_account_file(
  SERVICE_ACCOUNT_FILE,
  scopes=SCOPES
)

client = build('servicemanagement', 'v1', credentials=credentials).services()


def add_to_list(api_list, page_response):
    for api in page_response['services']:
        api_name = api['serviceName']
        api_list.append(api_name)


def list_services():
    apis = []

    page_request = client.list()
    page_response = page_request.execute()
    add_to_list(apis, page_response)

    while 'nextPageToken' in page_response.keys():
        page_request = client.list(pageToken=page_response['nextPageToken'])
        page_response = page_request.execute()
        add_to_list(apis, page_response)

    return apis


def get_config(service_name):
    config = client.getConfig(serviceName=service_name).execute()
    return config


if __name__ == "__main__":
    # apis = list_services()
    cloud_asset = get_config('cloudasset.googleapis.com')
    for api in cloud_asset['apis']:
        print(api)


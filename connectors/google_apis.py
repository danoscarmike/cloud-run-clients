import base64
import github3
import os
import yaml
import requests


# Authenticate with GitHub using Personal Access Token
g = github3.login(token=os.environ['GH_TOKEN'])
r = g.repository('googleapis', 'googleapis')


def list_apis():
    api_names = []
    c = r.directory_contents('google/cloud', return_as=dict)
    for file in c:
        if c[file].type == 'dir':
            api_names.append(file)
    return api_names


def list_api_versions(api):
    versions = []
    c = r.directory_contents(f'/google/cloud/{api}', return_as=dict)
    for file in c:
        if c[file].type == 'dir':
            versions.append(file)
    return versions


def get_api_details(api, version):
    api_title = api_summary = proto_url = None
    service_configs = [f'{api}_{version}.yaml',
                       f'{api}.yaml',
                       f'cloud{api}_{version}.yaml',
                       f'cloud{api}.yaml']
    c = r.directory_contents(f'/google/cloud/{api}/{version}', return_as=dict)
    for service_config in service_configs:
        if service_config in c:
            # TODO: use Github-Flask instead of rolling own with requests
            res = requests.get(c[service_config].git_url, auth=('danoscarmike',os.environ['GH_TOKEN']))
            if res.status_code == 200:
                proto_url = f'https://github.com/googleapis/googleapis/tree/master/google/cloud/{api}/{version}'
                content = res.json()['content']
                config_file = yaml.safe_load(base64.b64decode(content).decode('utf-8'))
                if 'title' in config_file:
                    api_title = config_file['title']
                if 'documentation' in config_file:
                    if 'summary' in config_file['documentation']:
                        api_summary = config_file['documentation']['summary']
            else:
                print(res.status_code)
    return api_title, api_summary, proto_url


if __name__ == '__main__':
    api = list_apis()[25]
    versions = list_api_versions(api)
    api_title, api_summary, proto_url = get_api_details(api, versions[0])
    print(api)
    print(versions)
    print(api_title)
    print(api_summary)
    print(proto_url)


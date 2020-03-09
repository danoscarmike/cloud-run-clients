import os
import tempfile

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    PATH_TO_API_COMMON_PROTOS = '/protos/'
    GOOGLEAPIS = '/googleapis/'
    UPLOAD_DIR = tempfile.mkdtemp(prefix='/tmp/', dir='/')
    DOWNLOAD_DIR = tempfile.mkdtemp(prefix='/tmp/', dir='/')
    CLIENT_DIR = tempfile.mkdtemp(prefix='/tmp/', dir='/')
    PROTO_DIR = tempfile.mkdtemp(prefix='/tmp/', dir='/')
    


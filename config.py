import os
import tempfile

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    PATH_TO_API_COMMON_PROTOS = '/protos/'
    GOOGLEAPIS = '/googleapis/'
    UPLOAD_DIR = os.path.join(os.getcwd(),"upload")
    DOWNLOAD_DIR = os.path.join(os.getcwd(),"download")
    CLIENT_DIR = os.path.join(os.getcwd(),"client")
    PROTO_DIR = os.path.join(os.getcwd(),"proto")
    


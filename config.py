import os
import tempfile

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    PATH_TO_API_COMMON_PROTOS = '/protos/'
    GOOGLEAPIS = '/googleapis/'
    UPLOAD_DIR = os.path.join(os.getcwd(),"upload")
    DOWNLOAD_DIR = os.path.join(os.getcwd(),"download")
    CLIENT_DIR = os.path.join(os.getcwd(),"client")
    PROTO_DIR = os.path.join(os.getcwd(),"proto")
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    


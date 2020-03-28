import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    GH_TOKEN = os.environ.get('GH_TOKEN')
    PATH_TO_API_COMMON_PROTOS = '/protos/'
    GOOGLEAPIS = '/googleapis/'
    UPLOAD_DIR = os.path.join(os.getcwd(), "upload")
    DOWNLOAD_DIR = os.path.join(os.getcwd(), "download")
    CLIENT_DIR = os.path.join(os.getcwd(), "client")
    PROTO_DIR = os.path.join(os.getcwd(), "proto")
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']

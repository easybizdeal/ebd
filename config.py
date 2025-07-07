import os

basedir = os.path.abspath(os.path.dirname(__file__))

import os

basedir = os.path.abspath(os.path.dirname(__file__))

import os

class Config:
    SECRET_KEY = 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Hostinger SMTP
    MAIL_SERVER = 'smtp.hostinger.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'amit.c@easybizdeal.com'
    MAIL_PASSWORD = 'Amit217698$1@'
    MAIL_DEFAULT_SENDER = 'Easy Biz Deal <amit.c@easybizdeal.com>'

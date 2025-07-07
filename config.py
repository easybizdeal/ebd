import os

basedir = os.path.abspath(os.path.dirname(__file__))

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'your_secret_key_here'
    # Store DB in /tmp for Render compatibility
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join('/tmp', 'easybiz.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Hostinger SMTP
    MAIL_SERVER = 'smtp.hostinger.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'amit.c@easybizdeal.com'
    MAIL_PASSWORD = 'Amit217698$1@'
    MAIL_DEFAULT_SENDER = 'Easy Biz Deal <amit.c@easybizdeal.com>'

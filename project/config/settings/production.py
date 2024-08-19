import os

from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    os.getenv('PUBLIC_IP'),
    os.getenv('DOMAIN_NAME'),
    os.getenv('WWW_DOMAIN_NAME'),
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_APP'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
    }
}

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# DEFAULT_FROM_EMAIL = None
# EMAIL_HOST = None
# EMAIL_PORT = None
# EMAIL_HOST_USER = None
# EMAIL_HOST_PASSWORD = None
# EMAIL_USE_TLS = None

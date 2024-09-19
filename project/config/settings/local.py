from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

MIDDLEWARE += [
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

INSTALLED_APPS += [
    'django_browser_reload'
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#SETTINGS FOR CELERY
CELERY_RESULT_BACKEND = 'django-db'
CELERY_BROKER_URL='redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT=['application/json']
CELERY_RESULT_SERIALIZER='json'
CELERY_TASK_SERIALIZER='json'

CELERY_BEAT_SCHEDULER='django_celery_beat.schedulers:DatabaseScheduler'


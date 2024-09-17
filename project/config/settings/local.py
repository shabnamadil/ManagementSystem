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


import os
from .settings import BASE_DIR

# E-Mail
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Authentication
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'

# URLs and directories
STATIC_ROOT = '../media_root/static/'
MEDIA_ROOT = '../media_root'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
STATICFILES_DIRS = [
    './mosta/static/',
]

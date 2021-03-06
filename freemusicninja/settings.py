"""
Django settings for freemusicninja project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os
import dj_database_url


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'SECRET KEY')

DEBUG = (os.environ.get('DJANGO_DEBUG', '').lower() != 'false')
USE_SSL = (os.environ.get('USE_SSL', '').lower() == 'true')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '.freemusic.ninja').split(':')

if DEBUG:
    CORS_ORIGIN_ALLOW_ALL = True
else:
    CORS_ORIGIN_WHITELIST = (
        'freemusic.ninja',
    )


ECHONEST_API_KEY = os.environ.get('ECHONEST_API_KEY', None)
JAMENDO_CLIENT_ID = os.environ.get('JAMENDO_CLIENT_ID', None)
FMA_API_KEY = os.environ.get('FMA_API_KEY', None)


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'djangosecure',
    'oauth2_provider',
    'raven.contrib.django.raven_compat',
    'relatives',
    'rest_framework',
    'rest_framework.authtoken',

    'artists',
    'bandcamp',
    'echonest',
    'fma',
    'similarities',
    'users',
)

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'djangosecure.middleware.SecurityMiddleware',
)

ROOT_URLCONF = 'freemusicninja.urls'

WSGI_APPLICATION = 'freemusicninja.wsgi.application'


DATABASES = {
    'default': dj_database_url.config(
        default='postgres://postgres:postgres@localhost/freemusicninja'
    ),
}

FIXTURE_DIRS = [os.path.join(BASE_DIR, 'fixtures')]

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

STATIC_URL = '/static/'
STATIC_ROOT = os.environ.get('DJANGO_STATIC_ROOT')


AUTH_USER_MODEL = 'users.User'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
}


# Security
SECURE_HSTS_SECONDS = 60  # Set to 518400 once this works
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_FRAME_DENY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_HTTPONLY = True

if USE_SSL:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'py.warnings': {
            'handlers': ['console'],
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    }
}

RAVEN_CONFIG = {
    'dsn': os.environ.get('RAVEN_CONFIG_DSN'),
}

try:
    BROKER_URL = os.environ['BROKER_URL']
except KeyError:
    CELERY_ALWAYS_EAGER = True
CELERY_TASK_SERIALIZER = 'json'

import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

sys.path.append(os.path.dirname(BASE_DIR))

from spirit.settings import *


"""
Django settings for checkio_forum project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vjb89i%v!xsyh%)(x-)ro0piq=28y5(5u_=9ee0xb0la=_!%0n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DOMAIN = 'forum.empireofcode.com'

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

_INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

INSTALLED_APPS += ('social.apps.django_app.default', )

_MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'checkio_forum.urls'

WSGI_APPLICATION = 'checkio_forum.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)


LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'checkio_forum.libs.social.backends.auth.CheckiOOAuth2',
)

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)


SOCIAL_AUTH_CHECKIO_NAME = 'checkio'
SOCIAL_AUTH_CHECKIO_KEY = ''
SOCIAL_AUTH_CHECKIO_SECRET = ''
SOCIAL_AUTH_CHECKIO_AUTHORIZATION_URL = 'https://www.checkio.org/oauth/authorize/'
SOCIAL_AUTH_CHECKIO_ACCESS_TOKEN_URL = 'http://www.checkio.org/oauth/token/'
SOCIAL_AUTH_CHECKIO_USER_INFO_URL = 'http://www.checkio.org/oauth/information/'

MONITORING_QA_RECIPIENTS = ['qaforum@checkio.org']
MONITORING_QA_CATEGORIES = ['Bugs']

MONITORING_PR_READER = 'ryanmvachon@gmail.com'
MONITORING_PR_USERS = ['oduvan', 'bryukh', 'haidamak', 'nickcool']


try:
    from settings_local import *
except ImportError:
    pass

"""
Django settings for learning_platform project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
import re
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY_LP')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

INTERNAL_IPS = [
    '127.0.0.1',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Custom apps
    'auth_app.apps.AuthAppConfig',
    'learning.apps.LearningConfig',
    'api',
    # Third party apps
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'learning_platform.urls'


# Session settings

# Set sessions storing in file (db by default)
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'session_store'
# It breaks the session not in all browsers
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# Cookie lifetime in seconds (1209600 s. = 2 weeks by default)
SESSION_COOKIE_AGE = 60 * 60
# If False session saves only when it changes (False by default)
SESSION_SAVE_EVERY_REQUEST = False
# If True - cookie access only through https
SESSION_COOKIE_SECURE = False
# Sending cookies to other sites. 'Strict' - forbid it. (None by default)
SESSION_COOKIE_SAMESITE = 'Strict'

# Custom session settings for remember user after login
REMEMBER_KEY = 'is_remember'
SESSION_REMEMBER_AGE = 60 * 60 * 24 * 365  # 1 year

# Custom cookies settings
COOKIES_REMEMBER_AGE = 60 * 60 * 24 * 365  # 1 year

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'learning_platform.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'USER': os.environ.get('USER_DB'),
        'PASSWORD': os.environ.get('PASSWORD_DB'),
        'NAME': 'learning_platform_new',
        # Unification db query in one transaction for a controller performing. Effective for multiple queries
        'ATOMIC_REQUEST': False,
        'AUTOCOMMIT': True,
        'OPTIONS': {'charset': 'utf8mb4'},
        'TEST': {
            'NAME': 'learning_platform_new_test',
        },
    },

}

# Caches settings
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'redis://:{REDIS_PASSWORD}@127.0.0.1:6379/0',
    },
    'session_store': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'redis://:{REDIS_PASSWORD}@127.0.0.1:6379/1',
    }
}
# For overall site caching on server
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 600
CACHE_MIDDLEWARE_KEY_PREFIX = ''

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

SHORT_DATETIME_FORMAT = 'j.m.Y H:I'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = BASE_DIR / 'static'
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static/img',
    BASE_DIR / 'static/styles',
    BASE_DIR / 'static/scripts',
]

# Media files
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Use custom model instead the default
AUTH_USER_MODEL = 'auth_app.User'


# For authenticate control
# If user is not logged in, redirect to 'login' url
LOGIN_URL = 'login'
# If user authenticate successful, redirect to 'index' url
LOGIN_REDIRECT_URL = 'index'
# If user log out, redirect to 'logout' url
LOGOUT_URL = 'logout'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'

# TLS use specified port 587
EMAIL_PORT = 587
# Enable encryption protocol
EMAIL_USE_TLS = True


EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# This email must be set for admins and managers mailing
SERVER_EMAIL = EMAIL_HOST_USER
# Admin email
LEARNING_ADMIN_EMAIL = os.environ.get('LEARNING_ADMIN_EMAIL')
ADMINS = [
    ('Alex', LEARNING_ADMIN_EMAIL),
]
MANAGERS = [
    ('Alex', LEARNING_ADMIN_EMAIL),
]

# How long reset password link in password_reset_email.html will exist
PASSWORD_RESET_TIMEOUT_DAYS = 1

# Pagination of main page settings
DEFAULT_COURSES_ON_PAGE = 4


# Production security settings

# Redirect to https connection on trying to get access through http
SECURE_SSL_REDIRECT = False
# Cookies through https
CSRF_COOKIE_SECURE = False
# How long access through https is available
# SECURE_HSTS_SECONDS = 0



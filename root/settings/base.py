"""
Django settings for root project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.core.urlresolvers import reverse_lazy

env = environ.Env(
    DEBUG=(bool, True),
    SECRET_KEY=(str, '#3pw2ogg-#q7r%abn2sy+zsaqnek2tp7g@ke+za46)#hb+pbka'),
    ALLOWED_HOSTS=(str, ''),
    DATABASE_URL=(str, 'sqlite:///sqlite.db'),
    EMAIL_URL=(str, ''),
    DEFAULT_FROM_EMAIL=(str, 'admin@domain.com'),
    HEADER_POST_ID=(int, 1),
    HEADER_PROGRESS_ID=(int, 1)
)
ENV = env  # so it will be copied to django.conf.settings
env.read_env('.env')

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
root = environ.Path(__file__) - 3
BASE_DIR = root()
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env('ALLOWED_HOSTS')
ALLOWED_HOSTS = ALLOWED_HOSTS.split(',') if ALLOWED_HOSTS else []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # The Django sites framework is required
    'django.contrib.sites',

    'django_extensions',
    'djcelery_email',
    'ckeditor',
    'ckeditor_uploader',

    'accounts',
    'common',
    'progress',
    'blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'root.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'common.context_processors.site_name',
                'common.context_processors.django_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'root.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': env.db()
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = 'static'
STATIC_URL = '/static/'

AUTH_USER_MODEL = 'accounts.User'

SITE_NAME = os.getenv('SITE_NAME', 'Django')
SITE_ID = 1

TEST_RUNNER = 'common.tests.core.DjangoNoseTestSuiteRunner'

LOGIN_URL = reverse_lazy('account_login')
LOGOUT_URL = reverse_lazy('account_logout')
LOGIN_ERROR_URL = reverse_lazy('account_login')
LOGIN_REDIRECT_URL = reverse_lazy('accounts:profile')

vars().update(env.email(backend='djcelery_email.backends.CeleryEmailBackend'))
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True


# CKEDITOR https://github.com/django-ckeditor/django-ckeditor
CKEDITOR_UPLOAD_PATH = "uploads/"


# WEBSITE CONFIG
HEADER_POST_ID = env('HEADER_POST_ID')
HEADER_PROGRESS_ID = env('HEADER_PROGRESS_ID')

"""
Django settings for mdp project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEOIP_PATH = os.path.join(BASE_DIR, 'geoip')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n)2e%(gfk4%9!2xq9zt$tbr7_crsk_lo6k^g*71q)9%-u=mopf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# import mimetypes
# mimetypes.add_type("text/css", ".css", True)

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'import_export',
    'django_user_agents',
    'mdp',
    'django.contrib.staticfiles',
    # the debug_toolbar will be useful for checking what is causing the most delay in page loading. Used only in debug
    # mode
    'debug_toolbar',
    'tracking_analyzer'
]

# Will be used to check what IPs can view the debug toolbar
INTERNAL_IPS = ['127.0.0.1',]

# This setting needs to be specified if you don't want all the built-in panels provided by the debug toolbar
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

ROOT_URLCONF = 'DB4MDP_NEW.urls'
MEDIA_ROOT = '/home/sharpfawkes/PycharmProjects/DB4MDP_NEW/static'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': ['/home/db4mdp/templates/'],
        'DIRS': ['/home/sharpfawkes/PycharmProjects/DB4MDP_NEW/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],

            'libraries': {
                'mdp_filters': 'mdp.templatetags.filters',
            }
        },
    },
]

WSGI_APPLICATION = 'DB4MDP_NEW.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# database_url = os.environ['DATABASE_URL']
# DATABASES = {
# 'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'ADAPTER': 'postgresql',
#        'NAME': 'postgres',
#        'USER': 'postgres',
#        'HOST': '/tmp',
#        'PORT': '5555'
#        }
#    }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'ADAPTER': 'postgresql',
        'NAME': 'ugwpwnay',
        'USER': 'ugwpwnay',
        'HOST': 'rajje.db.elephantsql.com',
        'PASSWORD': 'HoTRqVJKlgRFIMdcMXWbDBh3bYTm5pl9',
        'PORT': '5432'
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True

IMPORT_EXPORT_USE_TRANSACTIONS = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

# For dev server. Otherwise static files wont update
STATIC_URL = '/static/'
STATIC_ROOT = '/home/sharpfawkes/PycharmProjects/DB4MDP_NEW/staticfiles/'

# This list contains directories of where django will seach for additional static files other than static_root
# since we don't have any other static folders, I'm leaving it blank
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


# For production

# STATIC_URL = '/home/db4mdp/static/'

# STATICFILES_DIRS = [
#	os.path.join(BASE_DIR, "static"),
#	'/home/db4mdp/static/'
# ]

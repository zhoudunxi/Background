"""
Django settings for release_sdjj project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hganqtqwnh=454kn_iyx!@=hx0i@0%ip7+vgwj0ve4i)5z!&2v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

#ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['8.8.8.91']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'login',
    'release',
    'listrequest',
    'project_manegement',
    'apkbuild',
    'setting',
    'apphelp',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'release_sdjj.urls'

TEMPLATE_DIRS=( os.path.join(BASE_DIR,'templates'),)

WSGI_APPLICATION = 'release_sdjj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
      #  'ENGINE': 'django.db.backends.sqlite3',
      # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	'ENGINE': 'django.db.backends.mysql',
        'NAME': 'release_sdjj',
        'USER':'webadmin',
        'PASSWORD':'9527h1!f',
        'HOST':'8.8.8.90',
        'PORT':'3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = ''  
STATIC_URL = '/static/'  
STATICFILES_DIRS = (os.path.join(os.path.dirname(__file__), '../static/').replace('\\','/'),)

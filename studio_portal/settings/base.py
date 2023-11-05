"""
Django settings for studio_portal project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from .auth import *
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
env = os.getenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

APPS = [
    'apps.account',
    'apps.job'
]

THIRD_PARTY_APPS = [
    'drf_yasg',
    'django_filters',
    'storages',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'django_admin_select2',
    "corsheaders",
    # 'background_task',
    'multiupload'
]

INSTALLED_APPS = DJANGO_APPS + APPS + THIRD_PARTY_APPS

ROOT_URLCONF = 'studio_portal.urls'
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')
# STATIC_ROOT = os.path.join(BASE_DIR,'static/')
STATIC_DIR = os.path.join(BASE_DIR,'static')
STATICFILES_DIRS = [
    STATIC_DIR,
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{
                'custom_tags': 'apps.job.templatetags.custom_tags',
            }
        },
    },
]

WSGI_APPLICATION = 'studio_portal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': env('DB_NAME'),
       'USER': env('DB_USER'),
       'PASSWORD': env('DB_PASSWORD'),
       'HOST': env('DB_HOST'),
       'PORT': env('DB_PORT'),
   }
}

AUTH_USER_MODEL='account.Account'

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'utils.common.TemplateErrorMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    #'drf_user_activity_tracker.middleware.activity_tracker_middleware.ActivityTrackerMiddleware',
]


SWAGGER_SETTINGS = {
    'SHOW_REQUEST_HEADERS': True,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': True,
    'JSON_EDITOR': True,
    'SUPPORTED_SUBMIT_METHODS': [
        'get',
        'post',
        'put',
        'delete',
        'patch'
    ],
    'TAGS_SORTER': 'alpha',
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
#Email configuration
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST= env('MAIL_SERVER')
EMAIL_PORT= env('MAIL_PORT')
EMAIL_HOST_USER= env('EMAIL_USER')
EMAIL_HOST_PASSWORD= env('MAIL_PASSWORD')
EMAIL_USE_TLS=True
LINODE_BUCKET = 'sewrobj'
LINODE_BUCKET_REGION = env('LINODE_BUCKET_REGION')
LINODE_BUCKET_ACCESS_KEY = env('LINODE_BUCKET_ACCESS_KEY')
LINODE_BUCKET_SECRET_KEY = env('LINODE_BUCKET_SECRET_KEY')
AWS_S3_ENDPOINT_URL=f'https://{LINODE_BUCKET}.{LINODE_BUCKET_REGION}.linodeobjects.com' 
AWS_MAIN_S3_ENDPOINT_URL=f'https://{LINODE_BUCKET_REGION}.linodeobjects.com'
#AWS_S3_ENDPOINT_URL= 'sewrobj.us-east-1.linodeobjects.com'
AWS_ACCESS_KEY_ID=LINODE_BUCKET_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=LINODE_BUCKET_SECRET_KEY
AWS_S3_REGION_NAME=LINODE_BUCKET_REGION
AWS_S3_USE_SSL=True
AWS_STORAGE_BUCKET_NAME=LINODE_BUCKET
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_UPLOAD_AUTH = {
    'aws_access_key_id': env('LINODE_BUCKET_ACCESS_KEY'),
    'aws_secret_access_key': env('LINODE_BUCKET_SECRET_KEY')
}
LOGIN_REDIRECT_URL = "/"

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8001",
    "http://10.10.0.184:8001",
]
# CORS_ALLOW_ALL_ORIGINS = False

# CORS_ALLOW_METHODS = (
#     "DELETE",
#     "GET",
#     "POST",
#     "PUT",
# )

# CORS_ALLOW_HEADERS = (
#     "accept",
#     "authorization",
#     "content-type",
#     "user-agent",
#     "x-csrftoken",
#     "x-requested-with",
# )
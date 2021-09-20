"""
Django settings for wtd project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q1(lqb4(qh1gje2p=@@bo4oh-2nek9_mnxujpc71^c@d2#s8r6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework.authtoken',
    'rest_framework',
    # 'django_otp',
    # 'django_otp.plugins.otp_totp',
    # 'django_otp.plugins.otp_static',
    # 'drf_yasg',
    # 'polymorphic',
    'accounts',
    'orders.apps.OrdersConfig',
    'otp.apps.OtpConfig',
    # 'channels',
    'simple_history',
    'payments',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASSES':
        'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 30,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',  # To be removed later
        'rest_framework.authentication.SessionAuthentication',
    ]


}

AUTHENTICATION_BACKENDS = (
    ('django.contrib.auth.backends.ModelBackend'),
)

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'wtd.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'wtd.wsgi.application'
# ASGI_APPLICATION = 'wtd.asgi.application'
# ASGI_APPLICATION = "wtd.routing.application"
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             # "hosts": [('127.0.0.1', 6379)],
#             "hosts": [("redis", 6379)],
#         },
#     },
# }

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_BEAT_SCHEDULE = {
    'delete_expired_otp': {
        'task': 'otp.tasks.otp_handle',
        'schedule': float(os.getenv('CELERY_BEAT_SCHEDULE', '30.0')),
    },
    'delete_inactive_users': {
        'task': 'otp.tasks.inActive_users_handle',
        'schedule': float(os.getenv('CELERY_BEAT_SCHEDULE', '5.0')),
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('USER_EMAIL', 'pbblsspprt@gmail.com')
EMAIL_HOST_PASSWORD = os.getenv('USER_EMAIL_PASSWORD', 'QAZqaz@123')
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

#
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('database', 'postgres'),
        'USER': os.getenv('username', 'doadmin'),
        'PASSWORD': os.getenv('password', 'vwhQkTCyZoZ81FUg'),
        'HOST': os.getenv('host', 'db-postgresql-fra1-45029-do-user-8981715-0.b.db.ondigitalocean.com'),
        'PORT': os.getenv('port', '25060'),
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'SGBGPFRADB4OLGNOKLPL')
AWS_STORAGE_BUCKET_NAME = os.getenv(
    'AWS_STORAGE_BUCKET_NAME', 'filestorage-pubbles')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY',
                                  'irRJV3bQdNM6KFtTBniCpX1fU7jdaj5m3Ay1Y/tzfHY')
AWS_S3_REGION_NAME = 'fra1'
AWS_S3_ENDPOINT_URL = 'fra1.digitaloceanspaces.com'
AWS_S3_FILE_OVERWRITE = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
AUTH_USER_MODEL = 'accounts.User'
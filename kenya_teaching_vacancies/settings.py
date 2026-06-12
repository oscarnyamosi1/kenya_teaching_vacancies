from pathlib import Path
from datetime import timedelta
from corsheaders.defaults import default_headers
import os

from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback-change-in-production')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'
DEBUG= False

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY = "secret"

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',

    'api',
    'applications',
    'employers',
    'jobs',
    'main',
    'messagesapp',
    'payments',
    'schools',
    'superuser',
    'teachers'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'kenya_teaching_vacancies.urls'

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "kenyateachers.pythonanywhere.com",
    "www.kenyateachers.pythonanywhere.com"
]


CORS_ALLOWED_ORIGINS = [
    "https://kenyateachers.vercel.app",
    "http://localhost:5173",
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    "http://127.0.0.1:5173"

]

CORS_ALLOW_HEADERS = list(default_headers) + [
    "x-csrftoken"
]

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "https://kenyateachers.pythonanywhere.com",
    "https://kenyateachers.vercel.app",
    "http://localhost:5173",
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    "http://127.0.0.1:5173"
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'api.authentication.CookieJWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),

    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,

    'AUTH_HEADER_TYPES': ('Bearer',),
    "AUTH_COOKIE": "access_token",

    "AUTH_COOKIE_SECURE": True,
    "AUTH_COOKIE_HTTP_ONLY": True,
    "AUTH_COOKIE_SAMESITE": "None",
    
    "AUTH_COOKIE_PATH": "/",
}
COOKIE_SECURE = False #change to true in production

if DEBUG:
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = "Lax"

    CSRF_COOKIE_SECURE = False
    CSRF_COOKIE_SAMESITE="Lax"

    COOKIE_SAMESITE = 'Lax'

    SIMPLE_JWT.update({
        'AUTH_COOKIE_SECURE':False,
        'AUTH_COOKIE_SAMESITE':'Lax'
    })
else:
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None"

    COOKIE_SAMESITE = 'None'

    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_SAMESITE="None"

    SIMPLE_JWT.update({
        'AUTH_COOKIE_SECURE':True,
        'AUTH_COOKIE_SAMESITE':'None'
    })

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

COOKIE_PATH= "/"

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

ROOT_URLCONF = 'kenya_teaching_vacancies.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'kenya_teaching_vacancies.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



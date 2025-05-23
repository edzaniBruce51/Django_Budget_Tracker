from pathlib import Path
import os
from django.core.management.utils import get_random_secret_key
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# Use environment variable for SECRET_KEY if available, otherwise generate a random one
# This is more secure than hardcoding the secret key
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', get_random_secret_key())

# Set DEBUG based on environment variable
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

# Get port from environment variable, default to 8000
PORT = os.environ.get('DJANGO_PORT', 8000)

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    f'localhost:{PORT}',
    f'127.0.0.1:{PORT}',
    'django-budget-tracker.onrender.com',
    '.onrender.com',  #In case I decide to rename my service I will need this line since it allows all subdomains of onrender.com
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'finances',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# Always use SQLite for simplicity
# For development, store in the project directory
# For production (Render), store in a location that persists between deployments
if not DEBUG:  # In production (Render)
    # Create a directory that will persist between deployments
    sqlite_dir = os.path.join(BASE_DIR, 'data')
    os.makedirs(sqlite_dir, exist_ok=True)

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(sqlite_dir, 'db.sqlite3'),
        }
    }



STATIC_URL = 'static/'

# This production code might break development mode, so we check whether we're in DEBUG mode
if not DEBUG:
    # Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
    # and renames the files with unique names for each version to support long-term caching
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_DIRS = [BASE_DIR / 'static']

# Authentication settings
LOGIN_URL = 'finances:login'
LOGIN_REDIRECT_URL = 'finances:dashboard'
LOGOUT_REDIRECT_URL = 'finances:login'

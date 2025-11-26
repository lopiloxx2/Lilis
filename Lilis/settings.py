from pathlib import Path
import os

# Load environment variables from a local .env file when present to
# make it easy to persist SMTP and other secrets for development.
try:
    # python-dotenv is optional in production; if missing, continue using os.environ
    from dotenv import load_dotenv
    DOTENV_PATH = Path(__file__).resolve().parent.parent / '.env'
    if DOTENV_PATH.exists():
        load_dotenv(DOTENV_PATH)
except Exception:
    # If python-dotenv isn't installed, we silently continue — env vars can
    # still be provided through the environment as before.
    pass

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES_DIR = os.path.join(BASE_DIR,'templates')

STATIC_DIR = os.path.join(BASE_DIR,'static')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+w((lo!sp4k7x%(xg3s#cmv&)!0=ruy=c4#yjq85zfnjxdllsu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django_htmx",
    'productos',
    'proveedores',
    'login',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = 'Lilis.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'Lilis.context_processors.app_user',
            ],
        },
    },
]

WSGI_APPLICATION = 'Lilis.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lilis',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
    }
}

# Composite backend: sends via SMTP and also prints emails to console for local testing.
# Configure SMTP credentials using environment variables described below.
EMAIL_BACKEND = 'Lilis.email_backends.ConsoleAndSMTPBackend'

# SMTP settings (read from environment for security). Example env vars:
# SMTP_HOST=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USER=your_smtp_user
# SMTP_PASSWORD=your_smtp_password_or_app_password
# SMTP_USE_TLS=True
# SMTP_USE_SSL=False
EMAIL_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('SMTP_PORT', 587))
EMAIL_HOST_USER = os.environ.get('SMTP_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
EMAIL_USE_TLS = os.environ.get('SMTP_USE_TLS', 'True') == 'True'
EMAIL_USE_SSL = os.environ.get('SMTP_USE_SSL', 'False') == 'True'
EMAIL_FAIL_SILENTLY = os.environ.get('SMTP_FAIL_SILENTLY', 'False') == 'True'
EMAIL_TIMEOUT = int(os.environ.get('SMTP_TIMEOUT', '10'))

# Default from email: if not explicitly set, use the SMTP user (helps with providers
# like Gmail that require the From to match the authenticated account).
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL') or EMAIL_HOST_USER or 'no-reply@example.com'



# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es-cl'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [STATIC_DIR]

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login settings
LOGIN_URL = '/'
LOGOUT_REDIRECT_URL = '/'

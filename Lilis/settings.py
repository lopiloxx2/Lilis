from pathlib import Path
import os

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
    'login.middleware.PasswordChangeRequiredMiddleware',
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


# -----------------------------------------------------------------------------
# Security: cookie settings
# - `HttpOnly` evita acceso desde JavaScript (recomendado para cookies de sesión).
# - `Secure` obliga a enviar la cookie sólo por HTTPS (activar en producción).
# - `SameSite` ayuda a mitigar CSRF en peticiones cross-site ('Lax' es un buen balance).
# Ajustamos de forma condicional según `DEBUG` para evitar romper el desarrollo local.
# -----------------------------------------------------------------------------

# Recomendación: en producción `DEBUG` debe ser False y el sitio servido por HTTPS.
SESSION_COOKIE_HTTPONLY = True
# Marcar `Secure` sólo si no estamos en modo DEBUG (es decir, producción con HTTPS)
SESSION_COOKIE_SECURE = not DEBUG
# Opciones: 'Lax' (recomendado), 'Strict' o 'None' (si usas cross-site cookies con OAuth)
SESSION_COOKIE_SAMESITE = 'Lax'

# CSRF cookie: mantener accesible a JS si tu frontend la necesita; por seguridad mantenemos
# `Secure` sincronizado con `SESSION_COOKIE_SECURE` y `SameSite` en 'Lax'.
CSRF_COOKIE_SECURE = not DEBUG
# No poner CSRF_COOKIE_HTTPONLY = True salvo que no necesites leer el token en JS
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'

# Otras cabeceras de seguridad útiles
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Si quieres redirigir HTTP -> HTTPS en producción descomenta la siguiente línea
# SECURE_SSL_REDIRECT = not DEBUG

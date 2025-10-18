import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# ==========================
# Cargar variables .env
# ==========================
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

# ======================
# General
# ======================
SECRET_KEY = os.getenv("SECRET_KEY", "clave-de-desarrollo")
DEBUG = os.getenv("DEBUG", "True") == "True"
IS_PRODUCTION = not DEBUG

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS", "localhost,127.0.0.1"
).split(",")

# ======================
# Aplicaciones
# ======================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',
    'corsheaders',
    'drf_yasg',
    'rest_framework',
    'imagekit',
    'productos',
    'inventarios',
    'predicciones',
    'ventas',
    'usuarios',
    'compras',
    'core',
    'reportes',
    'knox',
    'django_rest_passwordreset',
    'django_filters',
    'simple_history',
    'django_extensions',
]

# ======================
# Middlewares
# ======================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'core.middleware.IdiomaPorHeaderMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ======================
# Seguridad en producción
# ======================
if IS_PRODUCTION:
    # Redirigir HTTP a HTTPS
    SECURE_SSL_REDIRECT = True

    # Cookies solo en HTTPS
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # Encabezado enviado por Railway para indicar HTTPS
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # HSTS opcional (cabeceras de seguridad extra)
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # CORS y CSRF de producción
    CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
    CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")

else:
    # CORS y CSRF para desarrollo
    CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
    CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000").split(",")


# ======================
# Autenticación
# ======================
AUTH_USER_MODEL = 'usuarios.Usuario'
AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]

# ======================
# URLs y Templates
# ======================
ROOT_URLCONF = 'django_crud_api.urls'

# ==========================
# Templates
# ==========================
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

# ==========================
# WSGI
# ==========================
WSGI_APPLICATION = 'django_crud_api.wsgi.application'

# ==========================
# REST Framework
# ==========================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('knox.auth.TokenAuthentication',),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# ======================
# Base de datos (PostgreSQL)
# ======================
DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}

# ==========================
# Validación de contraseñas
# ==========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ======================
# Archivos estáticos
# ======================
# Archivos estáticos (JS, CSS)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media (imágenes subidas por usuarios)
if IS_PRODUCTION:
    # En producción: usa el volumen montado
    MEDIA_URL = '/media/'
    MEDIA_ROOT = Path('/app/media')
else:
    # En desarrollo: usa la carpeta local
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

FILE_UPLOAD_TEMP_DIR = MEDIA_ROOT

# Configuración de almacenamiento
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

if IS_PRODUCTION:
    # Cache para archivos estáticos
    WHITENOISE_MAX_AGE = 31536000  # 1 año

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ======================
# Email
# ======================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

# ======================
# Internacionalización
# ======================
LANGUAGE_CODE = os.getenv("LANGUAGE_CODE", "es")
TIME_ZONE = os.getenv("TIME_ZONE", "America/La_Paz")
USE_I18N = True
USE_L10N = True
USE_TZ = os.getenv("USE_TZ", "False") == "True"
LANGUAGES = [('es', 'Español'), ('en', 'English')]
LOCALE_PATHS = [BASE_DIR / 'locale']

# # ======================
# # Seguridad en producción
# # ======================
# if IS_PRODUCTION:
#     SECURE_SSL_REDIRECT = True
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True
#     # Opcional: cabeceras extra de seguridad
#     SECURE_HSTS_SECONDS = 31536000
#     SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#     SECURE_HSTS_PRELOAD = True

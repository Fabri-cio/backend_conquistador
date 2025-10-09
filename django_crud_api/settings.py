from pathlib import Path
import dj_database_url
from dotenv import load_dotenv
import os

# ==========================
# Cargar variables .env
# ==========================
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================
# Configuración general
# ==========================
SECRET_KEY = os.getenv("SECRET_KEY", "clave-de-desarrollo")

# Detectar entorno: producción si no es localhost
IS_PRODUCTION = os.getenv("IS_PRODUCTION", "False") == "True"
DEBUG = not IS_PRODUCTION

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "localhost,127.0.0.1,web-production-87467.up.railway.app"
).split(",")

# ==========================
# Aplicaciones
# ==========================
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
    'cloudinary',
    'cloudinary_storage',
]

# ==========================
# Cloudinary
# ==========================
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
}
if IS_PRODUCTION:
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# ==========================
# Middlewares
# ==========================
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

# ==========================
# CORS y CSRF
# ==========================
CORS_ALLOWED_ORIGINS = os.getenv(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:5173,https://lovely-respect-production.up.railway.app"
).split(",")

CSRF_TRUSTED_ORIGINS = os.getenv(
    "CSRF_TRUSTED_ORIGINS",
    "http://*,https://web-production-87467.up.railway.app"
).split(",")

# ==========================
# Usuario personalizado
# ==========================
AUTH_USER_MODEL = 'usuarios.Usuario'
AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]

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
}

# ==========================
# Base de datos
# ==========================
DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_PUBLIC_URL'))
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

# ==========================
# Configuración de correo
# ==========================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

# ==========================
# Internacionalización
# ==========================
LANGUAGE_CODE = os.getenv("LANGUAGE_CODE", "es")
TIME_ZONE = os.getenv("TIME_ZONE", "America/La_Paz")
USE_I18N = True
USE_L10N = True
USE_TZ = os.getenv("USE_TZ", "False") == "True"

LANGUAGES = [('es', 'Español'), ('en', 'English')]
LOCALE_PATHS = [BASE_DIR / 'locale']

# ==========================
# Archivos estáticos y media
# ==========================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

if not IS_PRODUCTION:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
    FILE_UPLOAD_TEMP_DIR = BASE_DIR / 'media'

FILE_UPLOAD_MAX_MEMORY_SIZE = 2.5 * 1024 * 1024
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

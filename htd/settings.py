from pathlib import Path
from socket import gethostbyname, gethostbyname_ex, gethostname

import environ

from htd.version import __version__

env = environ.Env(DEBUG=(bool, False))
env.read_env(".env")


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET", default="ChangeMe")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")
ENV_NAME = env("ENV_NAME", default="local").lower()

ALLOWED_HOSTS = []
ALLOWED_HOSTS.extend(
    filter(None, [host.strip() for host in env("ALLOWED_HOSTS", default="").split(",")])
)
if env("AWS_EXECUTION_ENV", default=""):
    ALLOWED_HOSTS.append(gethostbyname(gethostname()))


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "nested_inline",
    "tinymce",
    "quizzes",
]
if DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
        "django_extensions",
    ]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
if DEBUG:
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")


ROOT_URLCONF = "htd.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "htd.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/static/"
MEDIA_URL = "/static/media/"

STATIC_ROOT = "/vol/web/static"
MEDIA_ROOT = "/vol/web/media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


##################################
# Django Rest Framework settings #
##################################
REST_FRAMEWORK = {
    "PAGE_SIZE": 30,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}


############################
# drf-spectacular settings #
############################
OPENAPI_ENABLED = env("OPENAPI_ENABLED", cast=bool, default=False)
if OPENAPI_ENABLED:
    INSTALLED_APPS.append("drf_spectacular")
    SPECTACULAR_SETTINGS = {
        "TITLE": "Twenty30 API",
        "DESCRIPTION": "Twenty30 API description",
        "VERSION": __version__,
        "SERVE_INCLUDE_SCHEMA": False,
        "COMPONENT_SPLIT_REQUEST": True,
        "ENUM_NAME_OVERRIDES": {},
    }


##################################
# Django Debug Toolbar settings #
##################################
if DEBUG:
    # for DjangoDebugToolbar and dockers
    hostname, _, ips = gethostbyname_ex(gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips]
    INTERNAL_IPS.extend(
        filter(
            None, [host.strip() for host in env("INTERNAL_IPS", default="").split(",")]
        )
    )

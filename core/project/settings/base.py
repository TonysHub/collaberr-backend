# flake8: noqa
SECRET_KEY = NotImplemented

DEBUG = False

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Collaberr apps
    "core.apps.accounts.apps.AccountsConfig",
    "core.apps.campaigns.apps.CampaignsConfig",

    # Third party apps
    "django_filters",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

DATABASES = {
   'default': {
      'ENGINE': 'django.db.backends.postgresql',
      'NAME': 'collaberr',
      'USER': 'postgres',
      'PASSWORD': 'collaberr',
      'HOST': 'localhost',
      'PORT': '5432',
      'ATOMIC_REQUESTS': True,
      'CONN_MAX_AGE': 60,
   }
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [(BASE_DIR / "core/templates")],  # type: ignore
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

WSGI_APPLICATION = "core.project.wsgi.application"

AUTH_USER_MODEL = "accounts.Account"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        # Implement this later
        # "OPTIONS": {"min_length": 8},

    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
    # Implement this later
    # {
    #     "NAME": "core.general.validators.PasswordValidator",
    # },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
      'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PARSER_CLASSES': ('rest_framework.parsers.JSONParser',),

}

SIMPLE_JWT = {
        'AUTH_HEADER_TYPES': ('Bearer',),
}

STATIC_ROOT = "/static/"
STATICFILES_DIRS = ((BASE_DIR / "core/static"),)  # type: ignore

MEDIA_ROOT = BASE_DIR / "core/media"  # type: ignore
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# URLS
LOGIN_REDIRECT_URL = "/"
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
ROOT_URLCONF = "core.project.urls"
CORS_ORIGIN_ALLOW_ALL = True

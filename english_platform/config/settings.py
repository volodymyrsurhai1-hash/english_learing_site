import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_path = BASE_DIR.parent / ".env"
load_dotenv(dotenv_path)

SECRET_KEY = os.environ.get("SECRET_KEY")

PATREON_WEBHOOK_SECRET: str = os.environ.get("PATREON_WEBHOOK_SECRET", "")

AI_PROVIDER: str = os.environ.get("AI_PROVIDER", "openai").lower()

OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL: str = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

GEMINI_API_KEY: str = os.environ.get("GEMINI_API", "")
GEMINI_MODEL: str = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")

DEBUG: bool = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")

ALLOWED_HOSTS: list[str] = [
    host.strip()
    for host in os.environ.get(
        "ALLOWED_HOSTS",
        "*" if DEBUG else "vsenglish.me,www.vsenglish.me,localhost,127.0.0.1",
    ).split(",")
    if host.strip()
]

CSRF_TRUSTED_ORIGINS: list[str] = [
    origin.strip()
    for origin in os.environ.get(
        "CSRF_TRUSTED_ORIGINS",
        "https://vsenglish.me,https://www.vsenglish.me,http://localhost,http://127.0.0.1",
    ).split(",")
    if origin.strip()
]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.core.apps.CoreConfig",
    "apps.dictionary.apps.DictionaryConfig",
    "apps.users.apps.UsersConfig",
    "apps.cards.apps.CardsConfig",
    "apps.grammar.apps.GrammarConfig",
    "apps.films.apps.FilmsConfig",
    "apps.subscriptions.apps.SubscriptionsConfig",
    "django_otp",
    "django_otp.plugins.otp_email",
    "django_otp.plugins.otp_totp",
    "django_otp.plugins.otp_static",
    "two_factor",
    "two_factor.plugins.email",
]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")
OTP_EMAIL_SENDER = os.environ.get("DEFAULT_FROM_EMAIL")


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "apps.core.middleware.EnforceOTPMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.subscriptions.context_processors.subscription_context",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "english_platform"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

AUTH_USER_MODEL = "users.User"
LOGIN_REDIRECT_URL = "dictionary:search"
LOGOUT_REDIRECT_URL = "dictionary:search"
LOGIN_URL = "two_factor:login"

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


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"

STATICFILES_DIRS: list[Path] = [
    BASE_DIR / "static",
]
STATIC_ROOT: Path = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = (
        os.environ.get("SECURE_SSL_REDIRECT", "True").lower() == "true"
    )
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

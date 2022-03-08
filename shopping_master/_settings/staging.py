# Staging Settings


SECRET_KEY = "-*5d2z+rw&xuqq*-v**bm1+5e^^2@u5x6x$!vm=8a9*%p@3bkx"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "shopping_master_staging",
        "USER": "shopping_master_staging",
        "PASSWORD": "shopping_master_staging",
        "HOST": "localhost",
        "PORT": "",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# TODO Change this when deploying to development
ALLOWED_HOSTS = ["*"]

CORS_ORIGIN_WHITELIST = "*"

GOOGLE_MAPS_API_KEY = ""

# Email settings
EMAIL_HOST = "email-smtp.ap-south-1.amazonaws.com"
EMAIL_PORT = 465
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = "Chip <thechip@curd.io>"
SERVER_EMAIL = "thechip911@curd.io"
EMAIL_SUBJECT_PREFIX = "[Chip ] "

# Development Settings

# TODO Change this when deploying to development
ALLOWED_HOSTS = ["*"]

# Setting for Sending Email Currently RAW Emails are Enabled
#  EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

CORS_ORIGIN_ALLOW_ALL = True

# Email settings
EMAIL_HOST = "email-smtp.ap-south-1.amazonaws.com"
EMAIL_PORT = 465
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = "Chip <thechip911@curd.io>"
SERVER_EMAIL = "thechip911@curd.io"
EMAIL_SUBJECT_PREFIX = "[Chip ] "

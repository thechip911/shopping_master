# Local System Settings
# Database Settings For Local if using Postgres
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "shopping_master_local",
#         "USER": "shopping_master_local",
#         "PASSWORD": "shopping_master_local",
#         "HOST": "localhost",
#         "PORT": "5432",
#     },
#     "test": {"NAME": "test_shopping_master_local"},
# }

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

from shopping_master.settings import BASE_DIR

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Production Setting

SECRET_KEY = "jrfwetghtu5%y2i*3yq6K_dj@lvlx&krlxn982u_poyl0(nx@0"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "shopping_master_production",
        "USER": "shopping_master_production",
        "PASSWORD": "shopping_master_production",
        "HOST": "localhost",
        "PORT": "",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# TODO Change this when deploying to development
ALLOWED_HOSTS = ["*"]

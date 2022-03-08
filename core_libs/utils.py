import os
import uuid

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def profile_picture_upload(instance, filename):
    """Set the profile picture Location in Account media"""
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    location = os.path.join("profiles/", "images/")
    return os.path.join(location, filename)


def send_email(email=None, template_name=None, data=None, subject=None):
    message = render_to_string(template_name, context={"data": data, "server_host": settings.API_BASE_URL})
    send_mail(
        subject,
        "msg_plain",
        settings.DEFAULT_FROM_EMAIL,
        [
            email,
        ],
        html_message=message,
    )

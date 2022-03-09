# python imports

# django imports
from django.contrib.auth import get_user_model

User = get_user_model()


# third-party imports

# local imports


class MobileOTPAuthenticationBackEnd(object):
    """
    Authenticates user based on given mobile_number and otp.
    """

    def authenticate(self, request, otp, email):
        try:
            user = User.objects.filter(email=email)
        except User.DoesNotExist:
            return None
        else:
            if user and user.otp(otp=otp, validate=True):
                return user
            return None

from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication


class CustomTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"

    def authenticate_credentials(self, key):
        model = self.get_model()

        try:
            token = model.objects.select_related("user").get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed("User Doesn't Exist")

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed("User is Blocked")

        if self.is_expired_token(token):
            raise exceptions.AuthenticationFailed("Authentication Token Expired")

        return token.user, token

    def is_expired_token(self, token):

        if (
            timezone.now()
            > timedelta(seconds=settings.AUTH_TOKEN_EXPIRATION_TIME_IN_SECONDS) + token.created
        ):
            return True

        return False

from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication


class CustomTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"

    def authenticate_credentials(self, key):
        model = self.get_model()

        try:
            token = model.objects.select_related("user").get(key=key)
        except model.DoesNotExist:
            return exceptions.AuthenticationFailed()

        if not token.user.is_active:
            return exceptions.AuthenticationFailed()

        if self.is_expired_token(token):
            pass

        return token.user, token

    def is_expired_token(self, token):
        pass

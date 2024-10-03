from rest_framework_simplejwt.authentication import JWTAuthentication

from .tokens import CustomAccessToken


class CustomJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        # Use the custom AccessToken class for validation
        return CustomAccessToken(raw_token)
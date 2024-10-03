from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

class CustomAccessToken(AccessToken):
    def verify(self):
        # Run the default access token verification first
        super().verify()

        # Get the jti of the access token
        jti = self.payload.get('jti')
        if not jti:
            raise InvalidToken("Token is missing the 'jti' claim.")

        # Check if the access token has been blacklisted
        if BlacklistedToken.objects.filter(token__jti=jti).exists():
            raise TokenError("This access token has been blacklisted.")

        # Check if the corresponding refresh token has been blacklisted
        refresh_jti = self.payload.get('refresh_jti')  # Assuming you stored this when issuing the tokens
        if refresh_jti and BlacklistedToken.objects.filter(token__jti=refresh_jti).exists():
            raise TokenError("This token's associated refresh token has been blacklisted.")
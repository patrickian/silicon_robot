from django.utils import timezone

from oauth2_provider.models import AccessToken, Application
from oauthlib.common import generate_token


class OAuthHandler:
    '''
        Handles custom creation of application and token
        OAUTH FLOW
        --> Create Application object
        --> Check client_secret for confirmation
        --> Creating AccessToken object
        --> Check expiration of AccessToken object whenever you login
        --> RefreshToken by updating existing AccessToken object
    '''
    def create_application(self, user):
        return Application.objects.create(
            user=user,
            client_type='confidential',
            authorization_grant_type='password',
            name=user.username
        )

    def __create_expiration(self):
        return timezone.now() + timezone.timedelta(days=1)

    def create_token(self, app):
        return AccessToken.objects.create(
            user=app.user,
            application=app,
            expires=self.__create_expiration(),
            token=generate_token()
        )

    def get_user_token(self, user, token=None):
        token_obj = AccessToken.objects.get(user=user)
        if token:
            return token_obj if token == token_obj.token else None
        else:
            return token_obj

    def validate_token(self, token):
        return (
            True if token.expires > timezone.now()
            else False
        )

    def refresh_token(self, user):
        token = self.get_user_token(user)

        if not self.validate_token(token):
            token.token = generate_token()
            token.expires = self.__create_expiration()
            token.save()
        return token

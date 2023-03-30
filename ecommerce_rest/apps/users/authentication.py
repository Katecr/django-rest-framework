from datetime import timedelta, datetime

from django.utils import timezone
from django.conf import settings
from django.contrib.sessions.models import Session

from rest_framework.authentication import TokenAuthentication


class ExpiringTokenAuthentication(TokenAuthentication):

    expired = False

    '''
    Calculate the expiration time with a variable from the base of the settings
    '''
    def expires_in(self,token):
        time_elapsed = timezone.now() - token.created
        left_time = timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
        return left_time

    '''
    Validates if the token has expired
    '''
    def is_token_expired(self, token):
        return self.expires_in(token) < timedelta(seconds = 0)

    '''
    Creates a variable called is_expire which verifies by means of the is_token_expired function, the elapsed time.
    '''
    def token_expire_handler(self,token):
        is_expire = self.is_token_expired(token)
        if is_expire:
            self.expired = True
            user = token.user
            # all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
            # if all_sessions.exists():
            #     for session in all_sessions:
            #         session_data = session.get_decoded()
            #         if user.id == int(session_data.get('_auth_user_id')):
            #             session.delete()
            token.delete()
            token = self.get_model().objects.create(user = user)
        
        return is_expire, token

    '''
    '''
    def authenticate_credentials(self,key):
        model = self.get_model()
        message, token, user = None, None, None
        try:
            token = model.objects.select_related('user').get(key=key)
            user = token.user
        except model.DoesNotExist:
            message = 'User inactive or invalid token'
            self.expired = True

        if token is not None:
            if not token.user.is_active:
                message = 'User inactive or invalid token'

            is_expired = self.token_expire_handler(token)

            if is_expired:
                message = 'Your token has expired'

        return (user, token, message, self.expired)
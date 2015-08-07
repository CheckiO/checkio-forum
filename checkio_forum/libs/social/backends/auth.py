import json
import urllib

from django.conf import settings
from social.backends.oauth import BaseOAuth2


class CheckiOOAuth2(BaseOAuth2):
    name = settings.SOCIAL_AUTH_CHECKIO_NAME
    AUTHORIZATION_URL = settings.SOCIAL_AUTH_CHECKIO_AUTHORIZATION_URL
    ACCESS_TOKEN_URL = settings.SOCIAL_AUTH_CHECKIO_ACCESS_TOKEN_URL
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE_SEPARATOR = ','
    REDIRECT_STATE = False
    STATE_PARAMETER = False
    ID_KEY = 'uid'

    EXTRA_DATA = [
        ('uid', 'uid'),
    ]

    def get_key_and_secret(self):
        return settings.SOCIAL_AUTH_CHECKIO_KEY, settings.SOCIAL_AUTH_CHECKIO_SECRET

    def get_user_details(self, response):
        return {'username': response.get('username'),
                'email': response.get('email') or ''}

    def user_data(self, access_token, *args, **kwargs):
        user_data_url = '?'.join([settings.SOCIAL_AUTH_CHECKIO_USER_INFO_URL,
                                  urllib.urlencode({'access_token': access_token})])
        try:
            return json.load(urllib.urlopen(user_data_url))
        except ValueError:
            return {}

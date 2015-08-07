SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)

SOCIAL_AUTH_CHECKIO_NAME = 'checkio'
SOCIAL_AUTH_CHECKIO_KEY = ''
SOCIAL_AUTH_CHECKIO_SECRET = ''
SOCIAL_AUTH_CHECKIO_AUTHORIZATION_URL = 'https://www.checkio.org/oauth/authorize/'
SOCIAL_AUTH_CHECKIO_ACCESS_TOKEN_URL = 'http://www.checkio.org/oauth/token/'
SOCIAL_AUTH_CHECKIO_USER_INFO_URL = 'http://www.checkio.org/oauth/information/'

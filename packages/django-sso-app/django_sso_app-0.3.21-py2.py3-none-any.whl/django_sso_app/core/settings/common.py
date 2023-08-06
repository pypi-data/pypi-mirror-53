from . import *


DJANGO_SSO_DEFAULT_CONSUMER_GROUP = env('DJANGO_SSO_DEFAULT_CONSUMER_GROUP', default="users")

DJANGO_SSO_CONSUMER_USERNAME_HEADER = env('DJANGO_SSO_CONSUMER_USERNAME_HEADER',
                                          default='HTTP_X_CONSUMER_USERNAME')
DJANGO_SSO_CONSUMER_GROUPS_HEADER = env('DJANGO_SSO_CONSUMER_GROUPS_HEADER',
                                        default='HTTP_X_CONSUMER_GROUPS')


_DJANGO_SSO_DEFAULT_FRONTEND_APP = 'django_sso_app.core.apps.frontend'
DJANGO_SSO_FRONTEND_APP = env('DJANGO_SSO_FRONTEND_APP', default=_DJANGO_SSO_DEFAULT_FRONTEND_APP)
DJANGO_SSO_HAS_CUSTOM_FRONTEND_APP = (DJANGO_SSO_FRONTEND_APP != _DJANGO_SSO_DEFAULT_FRONTEND_APP)


_DJANGO_SSO_APP_DEFAULT_USER_PROFILE = 'django_sso_app.backend.profiles'
DJANGO_SSO_APP_USER_PROFILE = env('DJANGO_SSO_APP_USER_PROFILE',
                                  default=_DJANGO_SSO_APP_DEFAULT_USER_PROFILE)  # patch
DJANGO_SSO_APP_USER_PROFILE_MODEL = env('DJANGO_SSO_APP_USER_PROFILE_MODEL',
                                        default=DJANGO_SSO_APP_USER_PROFILE + '.models.Profile')  # patch
DJANGO_SSO_APP_USES_EXTERNAL_USER_PROFILE = DJANGO_SSO_APP_USER_PROFILE is not None
DJANGO_SSO_APP_HAS_CUSTOM_USER_PROFILE = (DJANGO_SSO_APP_USER_PROFILE != _DJANGO_SSO_APP_DEFAULT_USER_PROFILE)
DJANGO_SSO_APP_SERVER = env.bool('DJANGO_SSO_APP_SERVER', default=False)


DJANGO_SSO_USER_FIELDS = (
    'username',
    'email',
)
DJANGO_SSO_REQUIRED_USER_FIELDS = env.list('DJANGO_SSO_REQUIRED_USER_FIELDS', default=DJANGO_SSO_USER_FIELDS)

DJANGO_SSO_PROFILE_ROLE_CHOICES = (
    (-1, 'Staff'),
    (0, 'Cityzen'),
    (1, 'Institutional'),
    (2, 'Professionist'),
    (4, 'Company'),
    (6, 'Istitutional Partition Item'),
    (7, 'App'),
)

DJANGO_SSO_PROFILE_FIELDS = (
    'role',
    'first_name', 'last_name',
    'description', 'picture', 'birthdate',
    'latitude', 'longitude',
    'country',
    'address',
    'language'
)
DJANGO_SSO_REQUIRED_PROFILE_FIELDS = env.list('DJANGO_SSO_REQUIRED_PROFILE_FIELDS', default=(
    #'role',
    #'first_name', #'last_name',
    #'description', 'picture', 'birthdate',
    #'latitude', 'longitude',
    #'country',
    #'address',
    #'language'
))

DJANGO_SSO_USER_CREATE_PROFILE_ON_SIGNUP = env.bool('DJANGO_SSO_USER_CREATE_PROFILE_ON_SIGNUP', default=True)

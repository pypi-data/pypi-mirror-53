from .common import *


DJANGO_SSO_SERVER_DOMAIN = env('DJANGO_SSO_SERVER_DOMAIN', default='localhost')
DJANGO_SSO_SERVER_PORT = env.int('DJANGO_SSO_SERVER_PORT', default=8000)

ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'
APP_DOMAIN = DJANGO_SSO_SERVER_DOMAIN + ':' + str(DJANGO_SSO_SERVER_PORT)

_SSO_DOMAINS = env('DJANGO_SSO_DOMAINS', default=DJANGO_SSO_SERVER_DOMAIN)
DJANGO_SSO_DOMAINS = _SSO_DOMAINS.split(',')
DJANGO_SSO_DOMAINS_DICT = {}
i=0
for el in DJANGO_SSO_DOMAINS:
    DJANGO_SSO_DOMAINS_DICT[el] = i
    i += 1

DJANGO_SSO_FULL_URLS_CHAIN = [ACCOUNT_DEFAULT_HTTP_PROTOCOL + '://' + el for el in DJANGO_SSO_DOMAINS]
DJANGO_SSO_URLS_CHAIN = [ACCOUNT_DEFAULT_HTTP_PROTOCOL + '://' + el for el in DJANGO_SSO_DOMAINS if el != APP_DOMAIN]
DJANGO_SSO_URLS_CHAIN_DICT = {}
i = 0
for el in DJANGO_SSO_URLS_CHAIN:
    DJANGO_SSO_URLS_CHAIN_DICT[el] = i
    i += 1

DJANGO_SSO_PASSEPARTOUT_PROCESS_ENABLED = len(DJANGO_SSO_URLS_CHAIN) > 0

DJANGO_SSO_DEFAULT_REFERRER = env('DJANGO_SSO_DEFAULT_REFERRER', default=ACCOUNT_DEFAULT_HTTP_PROTOCOL + '://' + APP_DOMAIN)

DJANGO_SSO_HIDE_PASSWORD_FROM_USER_SERIALIZER = env.bool('DJANGO_SSO_HIDE_PASSWORD_FROM_USER_SERIALIZER', default=True)

DJANGO_SSO_APIGW_ENABLED = env.bool('DJANGO_SSO_APIGW_ENABLED', default=False)
DJANGO_SSO_APIGW_HOST = env.bool('DJANGO_SSO_APIGW_HOST', default='kong')


DJANGO_SSO_BACKEND_CORE_APPS = [
    # 'django_sso_app.core.apps.users',
    'django_sso_app.core.apps.groups',
    'django_sso_app.core.apps.services',
    'django_sso_app.core.apps.devices',
    'django_sso_app.core.apps.passepartout',

    DJANGO_SSO_APP_USER_PROFILE,
    DJANGO_SSO_FRONTEND_APP
]

if DJANGO_SSO_APIGW_ENABLED:
    DJANGO_SSO_BACKEND_CORE_APPS += [
        'django_sso_app.core.apps.api_gateway.kong',
    ]

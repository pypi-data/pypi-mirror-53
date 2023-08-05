from django.conf import settings
from django.conf.urls import url
from django.urls import include


sso_app_urlpatterns = []

if settings.DJANGO_SSO_BACKEND_ENABLED:
    from django_sso_app.core.apps.groups.urls import urlpatterns as groups_urls
    from django_sso_app.core.apps.users.urls import urlpatterns as users_urls
    from django_sso_app.core.apps.services.urls import urlpatterns as services_urls
    from django_sso_app.core.apps.passepartout.urls import urlpatterns as passepartout_urls

    sso_app_urlpatterns += [
        url(r'^api/v1/auth/groups/', include((groups_urls, 'groups'), namespace="group")),
        url(r'^api/v1/auth/users/', include((users_urls, 'users'), namespace="user")),
        url(r'^api/v1/services/', include((services_urls, 'services'), namespace="service")),
        url(r'^api/v1/passepartout/', include((passepartout_urls, 'passepartout'), namespace="passepartout")),
    ]

    if not settings.DJANGO_SSO_APP_ENABLED and settings.DJANGO_SSO_APP_HAS_CUSTOM_USER_PROFILE:
        from django_sso_app.core.apps.profiles.urls import urlpatterns as profiles_urls

        sso_app_urlpatterns += [
            url(r'^api/v1/profiles/', include((profiles_urls, 'profiles'), namespace="profile")),
        ]

elif settings.DJANGO_SSO_APP_ENABLED and not settings.DJANGO_SSO_APP_HAS_CUSTOM_USER_PROFILE:
    from django_sso_app.core.apps.profiles.urls import urlpatterns as profiles_urls

    sso_app_urlpatterns += [
        url(r'^api/v1/profiles/', include((profiles_urls, 'profiles'), namespace="profile")),
    ]

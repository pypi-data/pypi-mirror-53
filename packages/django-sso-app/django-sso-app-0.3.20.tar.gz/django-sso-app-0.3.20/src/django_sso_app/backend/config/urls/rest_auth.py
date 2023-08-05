from django.conf.urls import url

from ...views.rest_auth import *


rest_auth_urlpatterns = [
    # rest_auth
    url(r'^api/v1/auth/registration/$', RegisterAPIView.as_view(), name='rest_register'),
    url(r'^api/v1/auth/verify-email/$', VerifyEmailAPIView.as_view(), name='rest_verify_email'),
    # completely overrided
    # url(r'^api/v1/auth/registration/', include('rest_auth.registration.urls')),

    # rest_auth
    url(r'^api/v1/auth/login/', LoginAPIView.as_view(), name='rest_login'),
    url(r'^api/v1/auth/logout/', LogoutAPIView.as_view(), name='rest_logout'),

    url(r'^api/v1/auth/user/', UserDetailsAPIView.as_view(), name='user_helper_view'),

    url(r'^api/v1/auth/password/reset/$', PasswordResetAPIView.as_view(), name='rest_password_reset'),
    url(r'^api/v1/auth/password/reset/confirm/$', PasswordResetConfirmAPIView.as_view(),
        name='rest_password_reset_confirm'),
    url(r'^api/v1/auth/password/change/$', PasswordChangeAPIView.as_view(),
        name='rest_password_change'),
    # completely overrided
    # url(r'^api/v1/auth/', include('rest_auth.urls')),
]

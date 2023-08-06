from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from ...views.allauth import *


allauth_urlpatterns = [
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        TemplateView.as_view(),
        name='restauth_password_reset_confirm'),

    # allauth
    url(r"^signup/$", SignupView.as_view(), name="account_signup"),
    url(r"^login/$", LoginView.as_view(), name="account_login"),
    url(r"^logout/$", LogoutView.as_view(), name="account_logout"),

    url(r"^password/change/$", login_required(PasswordChangeView.as_view()),
        name="account_change_password"),
    url(r"^password/set/$", login_required(PasswordSetView.as_view()), name="account_set_password"),

    url(r"^inactive/$", AccountInactiveView.as_view(), name="account_inactive"),

    # E-mail
    url(r"^email/$", login_required(EmailView.as_view()), name="account_email"),
    url(r"^confirm-email/$", EmailVerificationSentView.as_view(),
        name="account_email_verification_sent"),
    url(r"^confirm-email/(?P<key>[-:\w]+)/$", ConfirmEmailView.as_view(),
        name="account_confirm_email"),

    # password reset
    url(r"^password/reset/$", PasswordResetView.as_view(),
        name="account_reset_password"),
    url(r"^password/reset/done/$", PasswordResetDoneView.as_view(),
        name="account_reset_password_done"),
    url(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)/(?P<key>.+)/$",
        PasswordResetFromKeyView.as_view(),
        name="account_reset_password_from_key"),
    url(r"^password/reset/key/done/$", PasswordResetFromKeyDoneView.as_view(),
        name="account_reset_password_from_key_done"),
    # completely overrided
    # url(r'^$', include('allauth.urls')),
]

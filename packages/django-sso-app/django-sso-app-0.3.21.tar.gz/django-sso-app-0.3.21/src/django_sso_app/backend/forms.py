from django.conf import settings

from allauth.account.forms import SignupForm as allauth_SignupForm


if settings.DJANGO_SSO_USER_CREATE_PROFILE_ON_SIGNUP:
    from django_sso_app.core.apps.profiles.forms import ProfileForm

    class SignupForm(allauth_SignupForm, ProfileForm):
        def get_cleaned_data(self):
            return self.clean()
else:
    class SignupForm(allauth_SignupForm):
        def get_cleaned_data(self):
            return self.clean()

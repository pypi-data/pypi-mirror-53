from django.conf import settings
from django.urls import reverse


if settings.DJANGO_SSO_BACKEND_ENABLED:
    from django_sso_app.core.apps.users.models import AbstractUserModel

    class User(AbstractUserModel):
        pass

else:
    from django.contrib.auth.models import AbstractUser

    class User(AbstractUser):
        def get_absolute_url(self):
            return reverse("users:detail", kwargs={"username": self.username})

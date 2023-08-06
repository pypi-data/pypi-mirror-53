from rest_framework.urlpatterns import format_suffix_patterns

from django_sso_app.core.apps.profiles.urls import _urlpatterns


urlpatterns = format_suffix_patterns(_urlpatterns)

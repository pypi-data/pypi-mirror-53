from django.urls import path

from django_sso_app.backend.users.views import (
    user_redirect_view,
    user_update_view,
    user_detail_view,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="user.update"),
    path("<str:username>/", view=user_detail_view, name="user-detail"),
]

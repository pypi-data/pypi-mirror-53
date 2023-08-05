from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from ..services.views import SubscriptionApiViewSet
from .views import (CheckUserExistence,
                    UserApiViewSet,
                    UserUnsubscriptionApiView,
                    UserRevisionsApiView)

_urlpatterns = [
    url(r'^$', UserApiViewSet.as_view({'get': 'list'}), name="list"),

    url(r'^(?P<pk>[0-9A-Fa-f-]+)/$',
        UserApiViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}, name="detail"),
        name='detail'),


    url(r'^check/$',
        CheckUserExistence.as_view(), name="check_user_existence"),

    url(r'^revisions/$',
        UserRevisionsApiView.as_view(), name="users_revision"),

    url(r'^unsubscribe/$',
        UserUnsubscriptionApiView.as_view(),
        name='user_unsubscription'),


    url(r'^(?P<user_pk>[0-9A-Fa-f-]+)/subscriptions/$',
        SubscriptionApiViewSet.as_view({'get': 'list'}),
        name='user_subscriptions'),

    url(r'^(?P<user_pk>[0-9A-Fa-f-]+)/subscriptions/create/(?P<service_pk>\d+)/$',
        SubscriptionApiViewSet.as_view({'post': 'create'}),
        name='user_subscriptions_create'),

    url(r'^(?P<user_pk>[0-9A-Fa-f-]+)/subscriptions/(?P<pk>\d+)/$',
        SubscriptionApiViewSet.as_view({'get': 'retrieve'}),
        name='user_subscription_detail'),

    url(r'^(?P<user_pk>[0-9A-Fa-f-]+)/subscriptions/(?P<pk>\d+)/unsubscribe/$',
        SubscriptionApiViewSet.as_view({'post': 'unsubscribe'}),
        name='user_subscription_unsubscribe'),

]

urlpatterns = format_suffix_patterns(_urlpatterns)

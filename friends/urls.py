from django.conf.urls import url, include
from rest_framework import routers
from friends.views import FriendRequestView, FriendRequestRejectView, FriendRequestAcceptView, UserFriendListView, UserFollowerListView, UserFriendRequestView

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^friends/(?P<user_id>.+)/$', UserFriendListView.as_view()),
    url(r'^followers/(?P<user_id>.+)/$', UserFollowerListView.as_view()),
    url(r'^friendrequests/$', FriendRequestView.as_view({'get': 'list', 'post': 'create'})),
    url(r'^friendrequests/(?P<user_id>.+)/$', UserFriendRequestView.as_view()),
    url(r'^friendrequests/(?P<pk>.+)/update$', FriendRequestView.as_view({'put': 'update'})),
    url(r'^friendrequests/(?P<pk>.+)/delete$', FriendRequestView.as_view({'delete': 'destroy'})),
    url(r'^friendrequests/(?P<pk>.+)/reject$', FriendRequestRejectView.as_view()),
    url(r'^friendrequests/(?P<pk>.+)/accept$', FriendRequestAcceptView.as_view()),
]
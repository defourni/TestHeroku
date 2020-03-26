from django.conf.urls import url, include
from rest_framework import routers
from posts.views import PostViewSet, VisiblePostView, VisibleUserPostView

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^author/posts$', VisiblePostView.as_view()),
    url(r'^author/(?P<user_id>.+)/posts$', VisibleUserPostView.as_view()),
    # url(r'^friends/$', FriendView.as_view({'get': 'list', 'post': 'create'})),
    # url(r'^friends/(?P<pk>.+)/update$', FriendView.as_view({'put': 'update'})),
    # url(r'^friends/(?P<pk>.+)/delete$', FriendView.as_view({'delete': 'destroy'})),
    # url(r'^friends/(?P<pk>.+)/reject$', FriendRequestRejectView.as_view()),
    # url(r'^friends/(?P<pk>.+)/accept$', FriendRequestAcceptView.as_view()),
    # url(r'^friends/(?P<user_id>.+)/$', UserFriendListView.as_view()),
    # url(r'^followers/(?P<user_id>.+)/$', UserFollowerListView.as_view()),
    # url(r'^friend_requests/(?P<user_id>.+)/$', UserFriendRequestView.as_view()),
]
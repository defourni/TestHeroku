from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, generics, mixins
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.db.models import Q, Count
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from posts.models import Post
from posts.serializers import PostSerializer
from posts.permissions import IsAuthorOrReadOnly, PostVisibility

from friends.models import Friend

import sys
sys.path.append("..") 
import connection_helper as helper

def check_friend(author, user):
    num_friends = Friend.objects.filter(Q(followee=author) & Q(follower=user) & Q(mutual=True)).count()
    if num_friends == 0:
        return False

def check_FOAF(author, user):
    visible = check_friend(author, user)

    if not visible:             # if not friend, then check if they are FOAF
        author_friends = Friend.objects.filter(Q(followee=author) & Q(mutual=True))
        user_friends = Friend.objects.filter(Q(followee=user) & Q(mutual=True))

        for author_friend in author_friends:
            for user_friend in user_friends:
                if author_friend.follower == user_friend.follower:
                    return True
    else:
        return False

def get_visible_posts(posts, user):
    exclude_posts = []

    for post in posts:
        if post.author != user:
            if post.visibility == "PRIVATE":                # not author and the post is private
                exclude_posts.append(post.id)
            elif post.visibility == "FRIENDS" :             # not author and the post is friends visible
                visible = check_friend(post.author, user)
                if not visible:
                    exclude_posts.append(post.id)
            elif post.visibility == "FOAF":              # not author and the post is FOAF visible
                visible = check_FOAF(post.author, user)
                if not visible:
                    exclude_posts.append(post.id)
            # elif post.visibility == 5:              # not author and the post is another author visible
            #     if post.another_author != user:
            #         exclude_posts.append(post.id)
            # elif obj.visibility == 6:               # not author and the post is friends on same host visible
            #     # TODO: check friendship

    for exclude_post in exclude_posts:
        posts = posts.exclude(id=exclude_post)

    return posts

# code reference:
# Andreas Poyiatzis; https://medium.com/@apogiatzis/create-a-restful-api-with-users-and-jwt-authentication-using-django-1-11-drf-part-2-eb6fdcf71f45
class PostViewSet(viewsets.ModelViewSet):
    '''
    retrieve:
        Return a post instance.

        Permission:
            Any users: read only permission with posts shared with them

    list:
        Return all listed public posts.

        Permission:
            Any users: read only permission with posts shared with them

    create:
        Create a new post.

        Permission:
            Any users: write permission

    delete:
        Remove a existing post.

        Permission:
            Author: delete permission
            Other users: denied

    partial_update:
        Update one or more fields on a existing post.

        Permission:
            Author: write permission
            Other users: read only permission

        !! Currently DO NOT SUPPORT updating images of the post.
        !! DO NOT TRY updating images.

    update:
        Update a post.

        Permission:
            Author: write permission
            Other users: read only permission

        !! Currently DO NOT SUPPORT updating images of the post.
        !! DO NOT TRY updating images.
    '''
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly, PostVisibility)
    
    def get_serializer_class(self):
        # if self.action == 'create' or self.action == 'update':
        #     return PostSerializer
        # elif self.action == 'update':
        #     return FriendSerializer
        # return PostReadOnlySerializer
        return PostSerializer

    # associate Post with User
    # see more: https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/#associating-snippets-with-users
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request):
        queryset = Post.objects.filter(Q(visibility="PUBLIC") & Q(unlisted=False))
        serializer = self.get_serializer_class()(queryset, many=True, context={'request': request})

        remote_posts = helper.get_remote_posts("https://spongebook-develop.herokuapp.com")
        # return Response(serializer.data)
        return Response(serializer.data + remote_posts)

class VisiblePostView(generics.ListAPIView):
    '''
    Return all posts that visible to the currently authenticated user.
    '''

    # see more: https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-the-url
    serializer_class = PostSerializer
    permission_classes = (PostVisibility,)

    def get_queryset(self):
        if self.request.user.is_anonymous:      # to check if current user is an anonymous user first, since Q query cannot accept anonymous user
            return Post.objects.filter(Q(visibility="PUBLIC") & Q(unlisted=False))
        else:
            posts = get_visible_posts(Post.objects.filter(Q(unlisted=False)), self.request.user)
            return posts

class VisibleUserPostView(generics.ListAPIView):
    '''
    Return all posts of specified user that visible to the currently authenticated user.
    '''
    
    # see more: https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-the-url
    serializer_class = PostSerializer
    permission_classes = (PostVisibility,)

    def get_queryset(self):
        user_id = self.kwargs['user_id']

        if self.request.user.is_anonymous:      # to check if current user is an anonymous user first, since Q query cannot accept anonymous user
            return Post.objects.filter(Q(visibility="PUBLIC") & Q(author=user_id) & Q(unlisted=False))
        else:
            posts = get_visible_posts(Post.objects.filter(Q(author=user_id) & Q(unlisted=False)), self.request.user)
            return posts
from django.shortcuts import render
from rest_framework import viewsets, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.db.models import Q
from django.http import Http404, HttpResponseBadRequest
from friends.models import Friend
from friends.serializers import FriendSerializer, FriendReadOnlySerializer, FriendfollowerSerializer

from rest_framework.reverse import reverse

class FriendRequestView(mixins.CreateModelMixin, 
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    '''
    list:
        Return all friend requests of all users, ordered by friend request ID.

    create:
        Create a friend requests between two users (follow and send friend request).
        Status code "400 Bad Request" will be returned, if user field and friend field are same.

    delete:
        Remove a existing friend requests by friend requests ID (unfollow).
        Update the "mutual" field of the follower's friend requests to False.

    update:
        !! Do NOT use this API in the frontend.
        !! This API is only used for developing and testing.
        !! This API will be DEPRECATED!
        !! Update a friend requests.
    '''

    queryset = Friend.objects.all()
    # serializer_class = FriendReadOnlySerializer

    def get_object(self, pk):
        try:
            return Friend.objects.get(id=pk)
        except Friend.DoesNotExist:
            raise Http404

    def get_serializer_class(self):
        if self.action == 'create':
            return FriendfollowerSerializer
        elif self.action == 'update':
            return FriendSerializer
        return FriendReadOnlySerializer

    # def list(self, request):
    #     queryset = Friend.objects.all()
    #     # serializer = FriendReadOnlySerializer(queryset, many=True, context={'request': request})
    #     serializer = self.get_serializer_class()(queryset, many=True, context={'request': request})
    #     return Response(serializer.data)
    
    def create(self, request):
        serializer = self.get_serializer_class()(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        target = self.get_object(pk)

        if target.mutual:       # if target's mutual is True, set followee's mutual to False
            followee = Friend.objects.get(Q(followee=target.follower) & Q(follower=target.followee))
            followee_serializer = FriendSerializer(followee, data={"mutual": False}, partial=True)
            if followee_serializer.is_valid(raise_exception=True):      # have to call is_valid() before excution
                self.perform_update(followee_serializer)

        target.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FriendRequestRejectView(APIView):
    '''
    Reject the specified friend request.
    Update the "not_read" field of the friend requests with the specified ID to False.
    '''

    def get_object(self, pk):
        try:
            return Friend.objects.get(id=pk)
        except Friend.DoesNotExist:
            raise Http404
    
    def put(self, request, pk=None):
        target = self.get_object(pk)

        serializer = FriendSerializer(target, data={"not_read": False}, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):      # have to call is_valid() before excution
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FriendRequestAcceptView(APIView):
    '''
    Accept the specified friend request.
    Update the "mutual" field of the friend requests with the specified ID to True.
    Update the "not_read" field of the friend requests with the specified ID to False.
    '''

    def get_object(self, pk):
        try:
            return Friend.objects.get(id=pk)
        except Friend.DoesNotExist:
            raise Http404
    
    def put(self, request, pk=None):
        target = self.get_object(pk)

        # add the follower to the user's (followee) friend list
        follower_url = reverse('user-detail', args=[target.follower.id], request=request)
        followee_url = reverse('user-detail', args=[target.followee.id], request=request)
        mutual_data = {"followee": follower_url, "follower": followee_url, "mutual": True, "not_read": False}
        mutual_serializer = FriendSerializer(data=mutual_data)      # create a mutual following
        if mutual_serializer.is_valid(raise_exception=True):        # have to call is_valid() before excution
            mutual_serializer.save()

        serializer = FriendSerializer(target, data={"mutual": True, "not_read": False}, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):      # have to call is_valid() before excution
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserFriendListView(generics.ListAPIView):
    '''
    Return all friends of specified user_id.
    '''

    # see more: https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-the-url
    serializer_class = FriendReadOnlySerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Friend.objects.filter(Q(followee=user_id) & Q(mutual=True))

class UserFollowerListView(generics.ListAPIView):
    '''
    Return all followers of specified user_id.
    '''

    # see more: https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-the-url
    serializer_class = FriendReadOnlySerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Friend.objects.filter(Q(followee=user_id) & Q(mutual=False))

class UserFriendRequestView(generics.ListAPIView):
    '''
    Return all friend requests of specified user_id.
    '''

    # see more: https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-the-url
    serializer_class = FriendReadOnlySerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Friend.objects.filter(Q(followee=user_id) & Q(not_read=True))
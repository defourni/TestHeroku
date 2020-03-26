'''
Please NOTE:
    This permission file can only be used to restrict actions of users on the specifed object.
    If you want to only show specific objects as result to users, please use filters in the view.
    These permissions WOULD NOT BE EFFECTIVE to the filtered results return by queryset in the view.

    Which means: these permissions CAN ONLY REFUSE CERTAIN USER TAKE CERTAIN ACTIONS ON CERTAIN OBJECT,
    BUT CANNOT FILTER OBJECTS AS "GET" RESULT.
'''

from rest_framework import permissions
from django.db.models import Q
from friends.models import Friend

class IsAuthorOrReadOnly(permissions.BasePermission):
    '''
    Custom permission.
    Only the author of posts can edit or delete them.
    '''

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.author == request.user

class PostVisibility(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:      # is author
            return True
        elif obj.visibility == 2:           # not author and the post is private
            return False
        elif obj.visibility == 3:           # not author and the post is friends visible
            if request.user.is_anonymous:       # to check if current user is an anonymous user first, since Q query cannot accept anonymous user
                return False
            num_friends = Friend.objects.filter(Q(followee=obj.author) & Q(follower=request.user) & Q(mutual=True)).count()
            if num_friends > 0:
                return True
            else:
                return False
        # elif obj.visibility == 4:           # not author and the post is FOAF visible
        #     # TODO: check friendship
        elif obj.visibility == 5:           # not author and the post is another author visible
            # TODO: check author
            if obj.another_author == request.user:
                return True
        # elif obj.visibility == 6:           # not author and the post is friends on same host visible
        #     # TODO: check friendship
        else:                               # public
            return True
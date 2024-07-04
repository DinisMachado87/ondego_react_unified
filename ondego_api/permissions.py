from django.contrib.auth import get_user_model
from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist
from friends.models import Friend


class IsOwnerOrReadOnly(permissions.BasePermission):
    '''
    Only the owner can edit the object
    '''
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsFriendRequestedOrReadOnly(permissions.BasePermission):
    '''
    Only the to_user in the friend request can edit,
    but both the to_user and the owner can delete and view.
    '''
    def has_object_permission(self, request, view, obj):
        # Allow viewing for both the to_user and the owner
        if request.method in permissions.SAFE_METHODS:
            return obj.to_user == request.user or obj.owner == request.user
        # Allow delete for both the to_user and the owner
        elif request.method == 'DELETE':
            return obj.to_user == request.user or obj.owner == request.user
        # Allow all other modifications only for the to_user
        else:
            return obj.to_user == request.user


class IsFriendOwnerToDelete(permissions.BasePermission):
    '''
    Only the owner can see and delete the friend request
    '''
    def has_object_permission(self, request, view, obj):
        # Allow viewing and deleting only for the owner
        if request.method in permissions.SAFE_METHODS or request.method == 'DELETE':
            return obj.owner == request.user
        else:
            return False


class IsFriendToSeeAndOwnerToEditOrDelete(permissions.BasePermission):
    '''
    Only friends can see the events by a user 
    and only the owner can edit or delete
    '''

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Check if the request.user is a friend of the obj.owner
            try:
                Friend.objects.get(owner=obj.owner, friend=request.user)
                return True
            except ObjectDoesNotExist:
                pass
            return obj.owner == request.user
        else:
            return obj.owner == request.user

class IsFriendOfEventOwnerToSeeAndOwnerToEditOrDelete(permissions.BasePermission):
    '''
    Only friends of the owner of the event can see the comments by any user,
    but only the owner of the comment can edit or delete
    '''
    def has_object_permission(self, request, view, obj):
        # First check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            # Check if the request.user is a friend of the obj.owner
            try:
                Friend.objects.get(owner=obj.event.owner, friend=request.user)
                return True
            except ObjectDoesNotExist:
                pass
            return obj.owner == request.user
        else:
            return obj.owner == request.user

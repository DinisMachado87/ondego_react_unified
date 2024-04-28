from django.contrib.auth import get_user_model
from rest_framework import permissions


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
    Only the to_user in the friend request can edit
    but both the to_user and the owner can delete
    '''
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == 'DELETE':
            return obj.to_user == request.user or obj.owner == request.user
        else:
            return obj.to_user == request.user


class IsFriendOwnerToDelete(permissions.BasePermission):
    '''
    Only the owner can delete the friend request
    '''
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == 'DELETE':
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
            return obj.owner == request.user or request.user.id in obj.friend_ids
        return obj.owner == request.user

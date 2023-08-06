from rest_framework import permissions

from django.conf import settings

class PermissionDenied(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False


class IsAuthenticatedOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_authenticated == True



class IsAuthenticatedOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_authenticated == True


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user


class OwnerOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if obj == request.user:
            return True

        if getattr(obj, 'user', None) == request.user:
            return True

        return False
    

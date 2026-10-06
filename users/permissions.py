from typing import Any, cast
from rest_framework import permissions
from .models import UserProfile


class IsAdminRole(permissions.IsAdminUser):
    """
    Grants acccess only to users with ADMIN role / User status.
    """

    def has_permission(self, request, view) -> bool:
        user = cast(UserProfile, request.user)
        return bool(
            user and
            user.is_authenticated and
            user.is_admin
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow access (GET, HEAD, OPTIONS) to and authenticated user,
    But write operation (POST, PUT, PATCH, DELET) only **[Admins]**
    """

    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS',)

    def has_permission(self, request, view) -> bool:
        if request.method in self.SAFE_METHODS:
            return True
        user = cast(UserProfile, request.user)
        return bool(
            user and
            user.is_authenticated and
            user.is_admin
        )


class IsOwner(permissions.BasePermission):
    """
    Allow owners of an object to edit / delete it.
    """

    def has_object_permission(self, request, view, obj: Any):
        return obj.user == request.user

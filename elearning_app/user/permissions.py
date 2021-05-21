from rest_framework import permissions


class AdminOrIsOwnerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_superuser
        return True

    def has_object_permission(self, request, view, obj):
        return obj == request.user

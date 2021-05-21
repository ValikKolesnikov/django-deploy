from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        return user.is_staff
        

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_staff

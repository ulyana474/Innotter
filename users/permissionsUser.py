from rest_framework import permissions
from django.shortcuts import get_object_or_404
from users.models import User

class PermissionsForUserDependOnRole(permissions.BasePermission):

    def has_permission(self, request, view):
        user = get_object_or_404(User, pk=request.user_id)
        return user.is_authenticated

    def has_object_permission(self, request, view, obj):

        user = get_object_or_404(User, pk=request.user_id)
        if user.role == "admin":
            if request.method in permissions.SAFE_METHODS:
                return True
            if request.method == "PATCH":
                return True

        if request.user.is_superuser:
            return True

        return False

class PermissionsForAdminModerator(permissions.BasePermission):

    def has_permission(self, request, view):

        user = get_object_or_404(User, pk=request.user_id)
        if not user.is_authenticated:
            return False
        return user.role != User.Roles.USER

    def has_object_permission(self, request, view, obj):

        return True
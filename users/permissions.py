from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .models import User, Page

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        user = get_object_or_404(User, pk=request.user_id)
        if user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):

        user = get_object_or_404(User, pk=request.user_id)
        if user.role == "admin":
            if request.method == "PATCH":
                return True

        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.owner == user:
            return True

        return False

class IsOwnerOrReadOnlyForPost(permissions.BasePermission):

    def has_permission(self, request, view):

        user = get_object_or_404(User, pk=request.user_id)
        if user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):

        user = get_object_or_404(User, pk=request.user_id)
        if user.role == "admin":
            if request.method == "DELETE":
                return True

        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        page = get_object_or_404(Page, owner=request.user_id)
        if obj.page == page:
            return True

        return False
   
   
    
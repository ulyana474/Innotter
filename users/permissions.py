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
            if request.method in permissions.SAFE_METHODS:
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
        if user.role == "admin" or user.role == "moderator":
            if request.method == "DELETE":
                return True

        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        pages = Page.objects.filter(owner=user)
        if obj.page in pages:
            return True

        return False
   
   
    
from .views import * 
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("likedPosts", likedPosts),
]
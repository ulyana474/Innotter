from .views import * 
from django.urls import path, include
import pages
from pages import urls
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls))
]
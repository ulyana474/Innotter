from .views import * 
from django.urls import path, include
import pages
from pages import urls
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login', login),
    path('register',RegisterUserAPIView.as_view()),
    path("followToggle/<int:page_id>/", followToggle)
]
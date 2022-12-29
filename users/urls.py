from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import * 

router = DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login', login),
    path('register',RegisterUserAPIView.as_view()),
    path('search', search),
    path('news', news),
    path("followToggle/<int:page_id>/", followToggle),
    path("postLike/<int:post_id>", postLike),
    path("followRequests/<int:page_id>", followRequests),
    path("requestAccept/<int:page_id>/user/<int:user_id>", requestAccept),
    path("requestAccept/<int:page_id>/user", requestAccept),
]
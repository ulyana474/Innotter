from django.contrib import admin
from django.urls import path, include
from users import urls
from pages import urls
from posts import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('pages.urls')),
    path('', include('posts.urls')),
]
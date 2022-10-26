from django.urls import re_path
from . import views 

urlpatterns = [
    re_path('', views.post_list, name= 'post_list'),
    re_path(r'^search/', views.search, name= 'search'), 
    re_path(r'^post_list/', views.post_list, name= 'post_list'),
]
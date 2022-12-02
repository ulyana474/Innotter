from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.settings import EMAIL_HOST_USER
from app.tasks import send_mail_task
from .models import *
from .serializers import *
from rest_framework.viewsets import GenericViewSet
from users.permissions import *

class PostViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin):
    permission_classes = [IsOwnerOrReadOnlyForPost]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        page_id = request.data.get('page', -1)
        page = get_object_or_404(Page, pk=page_id)
        user = get_object_or_404(User, pk=request.user_id)
        if page.owner.id != request.user_id:
            return HttpResponseForbidden("not authenticated to create post on this page")
        content = request.data.get('content', '')
        if len(content) > 0:
            followers = page.followers.all()
            emails = list()
            for user in followers:
                emails.append(user.email)
            send_mail_task.delay(content, settings.EMAIL_HOST_USER, emails)
        return super().create(request, *args, **kwargs)

@api_view(["GET"])
def likedPosts(request):
    user = get_object_or_404(User, pk=request.user_id)
    posts = Post.objects.all()
    posts_to_show = list()
    for post in posts:
        likes = post.likes.all()
        if user in likes:
            posts_to_show.append(post)
    serializer = PostSerializer(posts_to_show, many=True)
    return Response(serializer.data)
  

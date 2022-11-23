from rest_framework import viewsets, mixins
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

  

from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet
from .models import *
from .serializers import *
from users.permissions import *

class PageViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Page.objects.all()
    serializer_class = PageSerializer
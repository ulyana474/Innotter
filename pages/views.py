from rest_framework import viewsets, mixins
from .models import *
from .serializers import *
from rest_framework.viewsets import GenericViewSet

class PageViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin):
    
    queryset = Page.objects.all()
    serializer_class = PageSerializer
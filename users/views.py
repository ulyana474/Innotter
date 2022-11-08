from rest_framework import viewsets, mixins
from .models import *
from .serializers import *
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view

class UserViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin):
    
    queryset = User.objects.all()
    
    serializer_class = UserSerializer
    
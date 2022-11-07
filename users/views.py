from rest_framework import viewsets, mixins
from .models import *
from .serializers import *
from rest_framework.viewsets import GenericViewSet

class UserViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *
from posts.serializers import *

class UserViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'delete':
            return [AllowAny(), ]        
        return super(UserViewSet, self).get_permissions()

    @action(methods=['get'], detail=False)
    def get(self, request):
        required_name = request.GET.get('name','')
        if(len(required_name) == 0):
            get_object_or_404(User, pk = 10)
            return Response({"result" : "enter name"})
        user = User.objects.filter(username=required_name)
        serializer = UserSerializer(user, many=True)
        return Response({"result": serializer.data})


class TagViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


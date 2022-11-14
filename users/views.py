from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from .models import *
from .serializers import *
from rest_framework.viewsets import GenericViewSet
from users.serializers import UserSerializer
from pages.serializers import PageSerializer

class UserViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def get_queryset(self):
    #     owner = self.kwargs['owner']
    #     return Page.objects.filter(page_owner=owner)

    @action(methods=['get'], detail=True)
    def page(self, request, pk=None):
        user = User.objects.get(pk=pk)
        page = Page.objects.filter(owner=pk)
        pages = user.pages.all()
        serializer = PageSerializer(pages, many=True)
        return Response({"result": serializer.data})
        
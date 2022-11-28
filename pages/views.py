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

    def create(self, request, *args, **kwargs):
        curr_user = get_object_or_404(User, pk=request.user_id)
        request.data['owner'] = curr_user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
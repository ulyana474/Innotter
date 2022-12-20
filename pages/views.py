from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from django.utils import timezone
from rest_framework import viewsets, mixins, filters, status
from rest_framework.decorators import action, parser_classes
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .models import *
from .serializers import *
from awsServices.statisticService.enums import PageMessageAction
from users.permissions import *
from users.permissionsUser import *
from users.models import Tag
from users.serializers import TagSerializer
from pages.producer import publish

class PageViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    user=None#for using in list() to pass to get_queryset()

    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'uuid', 'tags__name']

    def list(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, pk=request.user_id)
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        if self.user != None:
            if not self.user.role == User.Roles.ADMIN:
                return self.queryset.filter(is_private=False)
        return self.queryset

    def create(self, request, *args, **kwargs):
        curr_user = get_object_or_404(User, pk=request.user_id)
        request.data['owner'] = curr_user.id
        response = super().create(request, *args, **kwargs)
        publish({**response.data, PageMessageAction.NAME.value: PageMessageAction.CREATE.value})
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        publish({**response.data, PageMessageAction.NAME.value: PageMessageAction.UPDATE.value})
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PageSerializer(instance)
        publish({**serializer.data, PageMessageAction.NAME.value: PageMessageAction.DELETE.value})
        return super().destroy(request, *args, **kwargs)

    @action(methods=['PATCH'], detail=True)
    def tagCreate(self, request, pk=None):
        curr_page = get_object_or_404(Page, pk=pk)
        tag_name = request.GET.get('tag','')
        if len(tag_name) == 0:
            return Response({"tag name is empty"})
        if Tag.objects.filter(name = tag_name).exists():
            existing_tag = Tag.objects.get(name = tag_name)
            curr_page.tags.add(existing_tag)
        else:
            new_tag = Tag()
            new_tag.name = tag_name
            new_tag.save()
            Tag.objects.add(new_tag)
            curr_page.tags.add(new_tag)
        curr_page.save()
        serializer = PageSerializer(curr_page, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['PATCH'], detail=True)
    def tagDelete(self, request, pk=None):
        curr_page = get_object_or_404(Page, pk=pk)
        tag_name = request.GET.get('tag','')
        if len(tag_name) == 0:
            return Response({"tag name is empty"})
        if Tag.objects.filter(name = tag_name).exists():
            existing_tag = Tag.objects.get(name = tag_name)
            curr_page.tags.remove(existing_tag)
        curr_page.save()
        serializer = PageSerializer(curr_page, many=False)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    @action(methods=['PATCH'], detail=True)
    def blockPage(self, request, pk=None):
        user = get_object_or_404(User, pk=request.user_id)
        if user.role == User.Roles.ADMIN or user.role == User.Roles.MODERATOR:
            curr_page = get_object_or_404(Page, pk=pk)
            min = int(request.GET.get('min', '0'))
            hour = int(request.GET.get('hour', '0'))
            day = int(request.GET.get('day', '0'))
            delta = timedelta(days=10000000)#block permanent
            if min !=0 or hour != 0 or day != 0:
                delta = timedelta(days=day, minutes=min, hours=hour)
            now = timezone.now()
            block_time = now + delta
            curr_page.unblock_date = block_time
            curr_page.save()
            serializer = PageSerializer(curr_page, many=False)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return HttpResponseForbidden("Only admin or moderator can block page")
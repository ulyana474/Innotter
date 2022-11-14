from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

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

    @action(methods=['get'], detail=True)
    def pages(self, request, pk=None):
        user = User.objects.get(pk=pk)
        pages = user.pages.all()
        serializer = PageSerializer(pages, many=True)
        return Response({"result": serializer.data})

    @action(methods=['get'], detail=True)
    def user_page(self, request, pk=None):
        try:
            page_number = int(request.GET['page_number'])
            post_number = int(request.GET.get('post', '-1'))
            if(post_number < 0):
                user = User.objects.get(pk=pk)
                pages = user.pages.all()
                try:
                    page = pages[page_number]
                except IndexError as e:
                    content = {'page index': str(e)}
                    return Response(content, status=status.HTTP_404_NOT_FOUND)
                serializer = PageSerializer(page, many=False)
                return Response({"result": serializer.data})
            post_number = int(request.GET['post'])
        except ValueError as e:
            content = {"can't convert to integer": str(e)}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(pk=pk)
        pages = user.pages.all()
        serializer_post = PostSerializer()
        
        try:
            page = pages[page_number]
            posts = page.posts.all()
            try:
                post = posts[post_number]
            except IndexError as e:
                content = {'post index': str(e)}
                return Response(content, status=status.HTTP_404_NOT_FOUND)

            serializer_post = PostSerializer(post, many=False)
        except IndexError as e:
            content = {'page index': str(e)}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        return Response({"result": serializer_post.data})
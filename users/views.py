from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import exceptions, generics
from rest_framework import mixins, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from .models import *
from .serializers import *
from posts.serializers import *
from users.utils import generate_access_token, generate_refresh_token

class RegisterUserAPIView(generics.CreateAPIView):
  serializer_class = RegisterSerializer

@api_view(["POST"])
@ensure_csrf_cookie
def login(request):
    User = get_user_model()
    username = request.data.get('username')
    password = request.data.get('password')
    response = Response()
    if (username is None) or (password is None):
        raise exceptions.AuthenticationFailed(
            'username and password required')

    user = User.objects.filter(username=username).first()
    if(user is None):
        raise exceptions.AuthenticationFailed('user not found')
    if (not user.check_password(password)):
        raise exceptions.AuthenticationFailed('wrong password')

    serialized_user = UserSerializer(user).data

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
    response.data = {
        'access_token': access_token,
        'user': serialized_user,
    }

    return response

@api_view(["GET"])
def followToggle(request, page_id):
    page_obj = Page.objects.get(pk=page_id)
    curr_user = get_object_or_404(User, pk=request.user_id)
    if not curr_user.is_authenticated:
        return Response({"follow" : "not logged in"})
    if page_obj.is_private:
        if page_obj.follow_requests.filter(id=request.user_id).exists():
            page_obj.follow_requests.remove(request.user_id)
        else:
            page_obj.follow_requests.add(request.user_id)
    else:
        if page_obj.followers.filter(id=request.user_id).exists():
            page_obj.followers.remove(request.user_id)
        else:
            page_obj.followers.add(request.user_id)
    serializer = PageSerializer(page_obj, many=False)
    page_obj.save()
    return Response(serializer.data)

@api_view(["GET"])
def postLike(request, post_id):
    post_obj = get_object_or_404(Post, pk=post_id)
    if post_obj.likes.filter(id=request.user_id).exists():
        post_obj.likes.remove(request.user_id)
    else:
        post_obj.likes.add(request.user_id)
    serializer = PostSerializer(post_obj, many=False)
    post_obj.save()
    return Response(serializer.data)

class UserViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['get', 'post'], detail=False)
    def get(self, request):
        required_name = request.GET.get('name','')
        if(len(required_name) == 0):
            return Response({"result" : "name is empty"})
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


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
    followers = page_obj.followers.all()
    follow_requests = page_obj.follow_requests.all()
    if page_obj.is_private:
        f_requests = list(follow_requests)
        if curr_user in follow_requests:
            f_requests.remove(curr_user)
        else:
            f_requests.append(curr_user)
        page_obj.follow_requests.set(f_requests)
        serializer = PageSerializer(page_obj, many=False)
        page_obj.save()
        return Response(serializer.data)
    else:
        f = list(followers)
        if curr_user in followers:
            f.remove(curr_user)
        else:
            f.append(curr_user)
        page_obj.followers.set(f)
        serializer = PageSerializer(page_obj, many=False)
        page_obj.save()
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


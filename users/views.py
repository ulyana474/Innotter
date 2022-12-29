import os
from awsServices.s3Service.s3Manager import S3FileManager, S3Enums
from awsServices.statisticService.enums import PageMessageAction
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponseForbidden, HttpResponseRedirect
import json
import logging
from .models import *
from pages.producer import publish
from posts.serializers import *
import requests
from rest_framework import mixins, status, viewsets, exceptions, generics, permissions, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from .serializers import *
from users.utils import generate_access_token, generate_refresh_token
from users.permissionsUser import *

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

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
    page_obj = get_object_or_404(Page, pk=page_id)
    curr_user = get_object_or_404(User, pk=request.user_id)
    if not curr_user.is_authenticated:
        return HttpResponseForbidden("not logged in")
    if page_obj.owner == curr_user:
        return HttpResponseForbidden("can't subscribe to your own page")
    else:
        if page_obj.is_private:
            if page_obj.follow_requests.filter(id=request.user_id).exists():
                page_obj.follow_requests.remove(request.user_id)
                publish({PageMessageAction.KEY_PAGE_ID.value: page_id,
                         PageMessageAction.FIELD.value: "followers",
                         PageMessageAction.INCREASE.value: False,
                         PageMessageAction.NAME.value: PageMessageAction.UPDATE.value})
            else:
                page_obj.follow_requests.add(request.user_id)
                publish({PageMessageAction.KEY_PAGE_ID.value: page_id,
                         PageMessageAction.FIELD.value: "followers",
                         PageMessageAction.INCREASE.value: True,
                         PageMessageAction.NAME.value: PageMessageAction.UPDATE.value})
        else:
            if page_obj.followers.filter(id=request.user_id).exists():
                page_obj.followers.remove(request.user_id)
                publish({PageMessageAction.KEY_PAGE_ID.value: page_id,
                         PageMessageAction.FIELD.value: "followers",
                         PageMessageAction.INCREASE.value: False,
                         PageMessageAction.NAME.value: PageMessageAction.UPDATE.value})
            else:
                page_obj.followers.add(request.user_id)
                publish({PageMessageAction.KEY_PAGE_ID.value: page_id,
                         PageMessageAction.FIELD.value: "followers",
                         PageMessageAction.INCREASE.value: True,
                         PageMessageAction.NAME.value: PageMessageAction.UPDATE.value})
        serializer = PageSerializer(page_obj, many=False)
        page_obj.save()
        return Response(serializer.data)

@api_view(["GET"])
def followRequests(request, page_id):
    page_obj = get_object_or_404(Page, pk=page_id)
    if not page_obj.is_private:
        return HttpResponseForbidden("not private page - no follow requests")
    f_requests = page_obj.follow_requests.all()
    user_serializer = UserSerializer(f_requests, many=True)
    return Response(user_serializer.data)

@api_view(["GET"])
def postLike(request, post_id):
    post_obj = get_object_or_404(Post, pk=post_id)
    page = post_obj.page
    if post_obj.likes.filter(id=request.user_id).exists():
        post_obj.likes.remove(request.user_id)
        publish({PageMessageAction.KEY_PAGE_ID.value: page.id,
                 PageMessageAction.FIELD.value: "likes",
                 PageMessageAction.INCREASE.value: False,
                 PageMessageAction.NAME.value: PageMessageAction.UPDATE.value})
    else:
        post_obj.likes.add(request.user_id)
        publish({PageMessageAction.KEY_PAGE_ID.value: page.id,
                 PageMessageAction.FIELD.value: "likes",
                 PageMessageAction.INCREASE.value: True,
                 PageMessageAction.NAME.value: PageMessageAction.UPDATE.value})
    post_obj.save()
    serializer = PostSerializer(post_obj, many=False)
    return Response(serializer.data)

@api_view(["GET"])
def requestAccept(request, page_id, user_id=-1):
    page_obj = get_object_or_404(Page, pk=page_id)
    if not page_obj.is_private:
        return HttpResponseForbidden("not private page - no need to accept")
    f_requests = page_obj.follow_requests.all()
    if len(f_requests) == 0:
        return Response("no follow requests")
    if user_id == -1: #all users
        for user in f_requests:
            page_obj.followers.add(user)
        page_obj.follow_requests.clear() 
    else:
        if page_obj.follow_requests.filter(pk=user_id).exists():
            page_obj.followers.add(user_id)
            page_obj.follow_requests.remove(user_id)
    page_obj.save()
    serializer = PageSerializer(page_obj, many=False)
    return Response(serializer.data)

@api_view(["GET"])
def search(request):
    findBy = request.GET.get('findBy', '')
    search = request.GET.get('search', '')
    if findBy == 'page':
        return HttpResponseRedirect(f"http://127.0.0.1:8000/pages?search={search}")
    return HttpResponseRedirect(f"http://127.0.0.1:8000/users?search={search}")

@api_view(["GET"])
def news(request):
    user = get_object_or_404(User, pk=request.user_id)
    posts = Post.objects.order_by('updated_at').reverse()
    posts_to_show =  list()
    for post in posts:
        if post.page.owner == user:
            posts_to_show.append(post)
        elif user in post.page.followers.all():
            posts_to_show.append(post)
    serializer = PostSerializer(posts_to_show, many=True)
    return Response(serializer.data)

class UserViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin):
    permission_classes = [PermissionsForUserDependOnRole]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['username']

    def update(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user_id)
        if user.role == User.Roles.ADMIN:
            is_blocked = request.data.get('is_blocked', None)
            if not user.id == request.user_id:
                if is_blocked == None or len(request.data) > 1:
                    return HttpResponseForbidden("you can change only 'is_blocked' value")
        #check img extension
        img_path = request.data.get('image_s3_path', None)
        if img_path is not None:
            filename, file_extension = os.path.splitext(img_path)
            print(file_extension)
            if file_extension != '.jpg' and file_extension != '.png':
                return HttpResponseForbidden("you can download photo with '.jpg' or '.png' extension") 
            manager = S3FileManager()
            username = user.username
            obj_name = username + file_extension
            s3_path = f"S3://{S3Enums.BUCKET_NAME.value}/{obj_name}"
            resp_dict = manager.create_presigned_post(S3Enums.BUCKET_NAME.value, obj_name)
            if resp_dict is None:
                logger.info("response is None")
                exit(1)    
            request.data["image_s3_path"] = s3_path
            response = super().update(request, *args, **kwargs)
            response.data["presigned_url"] = resp_dict
        return response
        
class TagViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


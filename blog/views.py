from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.utils import timezone
from .models import Post
from django.core.exceptions import *

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date') #QuerySet
    return render(request, 'blog/post_list.html', {'posts': posts})

def search(request):
    if request.method == 'POST':
        search_id = request.POST.get('textfield', None)
    try:
            user = Person.objects.get(name = search_id)
            #do something with user
            html = ("<H1>%s</H1>", user)
            return HttpResponse(html)
    except Person.DoesNotExist:
            return HttpResponse("no such user")  
    else:
        return render(request, 'form.html')
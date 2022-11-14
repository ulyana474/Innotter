from rest_framework import serializers
from .models import User, Tag
from pages.serializers import PageSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','email', 'image_s3_path', 'role', 'title', 'is_blocked', 'pages')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name')
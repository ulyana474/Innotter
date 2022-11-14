from rest_framework import serializers
from .models import User
from pages.serializers import PageSerializer

class UserSerializer(serializers.ModelSerializer):
    pages = PageSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username','email', 'image_s3_path', 'role', 'title', 'is_blocked', 'pages')
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = Post
        fields = ('id', 'page', 'content', 'reply_to', 'likes', 'created_at', 'updated_at', 'username')

    def get_username(self, post):
        username = post.page.owner.username
        return username
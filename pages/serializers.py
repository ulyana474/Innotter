from rest_framework import serializers
from .models import Page

class PageSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = Page
        fields = ('id', 'name', 'uuid', 'description', 'tags', 'owner', 'followers', 'image', 'is_private', 'follow_requests', 'unblock_date', 'username')

    def get_username(self, page):
        username = page.owner.username
        return username
from django.db import models

class Post(models.Model):
    page = models.ForeignKey('pages.Page', on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=180)

    reply_to = models.ForeignKey('posts.Post', on_delete=models.SET_NULL, null=True, related_name='replies')
    likes = models.ManyToManyField('users.User', blank=True, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def number_of_likes(self):
        return self.likes.count()
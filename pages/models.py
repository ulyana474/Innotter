from django.db import models

class Page(models.Model):
    name = models.CharField(max_length=80)
    uuid = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    tags = models.ManyToManyField('users.Tag', blank=True, related_name='pages_tags')
    
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='pages')
    followers = models.ManyToManyField('users.User', blank=True, related_name='follows')

    image = models.URLField(null=True, blank=True)

    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField('users.User',  blank=True, related_name='requests')

    unblock_date = models.DateTimeField(null=True, blank=True)

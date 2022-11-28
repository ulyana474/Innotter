from celery import shared_task
import datetime
from django.shortcuts import get_object_or_404
from pages.models import Page

@shared_task
def check_unblock_pages():
    pages = Page.objects.all()
    for page in pages:
        if page.unblock_date is not None:
            unblock_date = page.unblock_date
            now = datetime.datetime.now()
            if unblock_date <= now:
                page.unblock_date = None
                page.save()
           
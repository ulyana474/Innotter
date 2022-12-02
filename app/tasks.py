from celery import shared_task
from datetime import timedelta
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
from pages.models import Page
from users.models import User

@shared_task
def check_unblock_pages():
    pages = Page.objects.all()
    for page in pages:
        if page.unblock_date is not None:
            unblock_date = page.unblock_date
            if unblock_date <= timezone.now():
                page.unblock_date = None
                page.save()

@shared_task
def send_mail_task(message, email_from, recepient_list):
    if len(recepient_list) > 0:
        send_mail("Innotter:new post", message, email_from, recepient_list)

@shared_task
def block_page_automatically(days_to_block=1000):
    users_blocked = User.objects.filter(is_blocked=True)
    now = timezone.now()
    delta = timedelta(days=days_to_block)
    for user in users_blocked:
        pages_to_block = user.pages.all()
        for page in pages_to_block:
            if page.unblock_date == None or page.unblock_date <= now:
                page.unblock_date = now + delta
                page.save()
            
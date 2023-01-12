import pytest
from django.urls import reverse
from faker import Faker
from rest_framework.test import APIClient
from pages.models import Page
from posts.models import Post
from users.models import User

fake = Faker()

register_url = reverse('register')
login_url = reverse('login')

@pytest.fixture
def api_client():
    return APIClient


@pytest.fixture()
def admin_client(api_client):
    admin_data={
    "email": "admin@gmail.com",
    "username": "admin",
    "password": "admin_password",
    "password2": "admin_password",
    "first_name": "eric",
    "last_name": "clapton"
    }
    client = api_client()
    present_admin = User.objects.filter(role='admin')
    if len(present_admin) == 0:
        register = client.post(register_url, admin_data, format="json")
    present_admin = User.objects.filter(username='admin').first()
    present_admin.role = User.Roles.ADMIN
    present_admin.save()
    login = client.post(login_url,
                        {'username': admin_data.get('username'),
                        'password': admin_data.get('password')},
                        format="json")
    token = login.data.get('access_token')
    client.credentials(HTTP_AUTHORIZATION=token)
    return client


@pytest.fixture()
def moderator_client(api_client):
    moderator_data={
    "email": "moderator@gmail.com",
    "username": "moderator",
    "password": "moderator_password",
    "password2": "moderator_password",
    "first_name": "moderator",
    "last_name": "moderator"
    }
    client = api_client()
    present_moderator = User.objects.filter(role='moderator')
    if len(present_moderator) == 0:
        register = client.post(register_url, moderator_data, format="json")
    present_moderator = User.objects.filter(username='moderator').first()
    present_moderator.role = User.Roles.MODERATOR
    present_moderator.save()
    login = client.post(login_url,
                        {'username': moderator_data.get('username'),
                        'password': moderator_data.get('password')},
                        format="json")
    token = login.data.get('access_token')
    client.credentials(HTTP_AUTHORIZATION=token)
    return client


@pytest.fixture()
def user_item():
    user = User.objects.create_user(username='test')
    user.save()
    return user


@pytest.fixture()
def user_item2():
    user = User.objects.create_user(username='test2', email='user2@gmail.com')
    user.save()
    return user


@pytest.fixture
def api_auth_client(api_client):
    client = api_client()
    user_data={
        'email': fake.email(),
        'username': fake.email().split('@')[0],
        'password': 'fake_password',
        'password2': 'fake_password',
        'first_name': fake.first_name(),
        'last_name': fake.last_name()
        }
    register = client.post(register_url, user_data, format="json")
    login = client.post(login_url, user_data, format="json")
    token = login.data.get('access_token')
    client.credentials(HTTP_AUTHORIZATION=token)
    return client


@pytest.fixture
def post_item(user_item):
    post = Post.objects.create(
        page=Page.objects.create(
            name=fake.email().split('@')[0],
            owner=user_item,
            ),
        content=fake.sentence()
        )
    post.save()
    return post


@pytest.fixture
def random_user_data():
    fake = Faker()
    user_data={
        'email': fake.email(),
        'username': fake.email().split('@')[0],
        'password': 'fake_password',
        'password2': 'fake_password',
        'first_name': fake.first_name(),
        'last_name': fake.last_name()
        }
    return user_data


@pytest.fixture
def page_item(user_item):
    page = Page.objects.create(
        name=fake.email().split('@')[0],
        owner=user_item
        )
    page.save()
    return page


@pytest.fixture
def page_item_with_follow_requests(page_item, api_client):
    page = page_item
    page.is_private = True
    follower = User.objects.get(username='test')
    page.follow_requests.add(follower.pk)
    page.save()
    return page


@pytest.fixture
def post_item_with_like(post_item, user_item2):
    post = post_item
    post.likes.add(user_item2.pk)
    return post
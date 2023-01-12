import pytest
from django.urls import reverse
from faker import Faker
from pages.models import Page
from posts.models import Post
from users.models import User

pytestmark = pytest.mark.django_db

register_url = reverse('register')
login_url = reverse('login')
fake = Faker()


user_data={
    'email': fake.email(),
    'username': fake.email().split('@')[0],
    'password': 'fake_password',
    'password2': 'fake_password',
    'first_name': fake.first_name(),
    'last_name': fake.last_name()
    }


def test_user_follow_requests(page_item_with_follow_requests, api_auth_client):
    view_requests_url = f'/followRequests/{page_item_with_follow_requests.pk}'
    response = api_auth_client.get(view_requests_url)
    assert response.status_code == 200


def test_user_can_search_user(api_auth_client, user_item):
    user_item
    username = 'test'
    redirect_search_url = f'/search?search={username}'
    response = api_auth_client.get(redirect_search_url)
    assert response.status_code == 302 #manual redirect
    search_url = f'/users/?search={username}'
    response = api_auth_client.get(search_url)
    assert response.status_code == 200
 

def test_user_can_search_pages(api_auth_client, page_item):
    page = page_item
    page_name = page.name
    redirect_search_url = f'/search?findBy=page&search={page_name}'
    response = api_auth_client.get(redirect_search_url)
    assert response.status_code == 302
    search_url = f'/pages/?search={page_name}'
    response = api_auth_client.get(search_url)
    assert response.status_code == 200


def test_user_accept_all_requests(page_item_with_follow_requests, api_auth_client):
    accept_url = f'/requestAccept/{page_item_with_follow_requests.pk}/user'
    response = api_auth_client.get(accept_url)
    assert response.status_code == 200


def test_user_list(api_auth_client):
    endpoint = reverse('user-list')
    client = api_auth_client
    response = client.get(path=endpoint)
    assert response.status_code == 200


def test_cant_login_without_username(api_client):
    user_data2 = {'password': user_data.get('password')}
    register = api_client().post(register_url, user_data, format="json")
    login = api_client().post(login_url, user_data2, format="json")
    assert login.status_code == 401


def test_cant_login_without_password(api_client):
    user_data2 = {'username': user_data.get('username')}
    register = api_client().post(register_url, user_data, format="json")
    login = api_client().post(login_url, user_data2, format="json")
    assert login.status_code == 401


def test_user_follow(page_item, api_auth_client):
    follow_url = f'/followToggle/{page_item.pk}/'
    response = api_auth_client.get(follow_url)
    assert response.status_code == 200


def test_user_like(post_item, api_auth_client):
    like_url = f'/postLike/{post_item.pk}'
    init_len = len(post_item.likes.all())
    response = api_auth_client.get(like_url)
    assert response.status_code == 200
    post = Post.objects.get(pk=post_item.pk)
    final_len = len(post.likes.all())
    assert final_len - init_len == 1


def test_user_cant_delete_anothers_post(api_auth_client, admin_user, post_item):
    pk = post_item.pk
    endpoint = f'/posts/{pk}/'
    response = api_auth_client.delete(path=endpoint)
    assert response.status_code == 401  #unauthorized


def test_admin_can_delete_posts(admin_client, post_item):
    pk = post_item.pk
    endpoint = f'/posts/{pk}/'
    response = admin_client.delete(path=endpoint)
    assert response.status_code == 204  #no content


def test_admin_can_block_page(admin_client, page_item):
    pk = page_item.pk
    endpoint = f'/pages/{pk}/blockPage/?min={5}'
    response = admin_client.get(path=endpoint)
    assert response.status_code == 202  #accepted


def test_admin_can_block_user(admin_client, user_item):
    pk = user_item.pk
    endpoint = f'/users/{pk}/'
    response = admin_client.patch(path=endpoint, data={"is_blocked": True}, format='json')
    assert response.status_code == 200


def test_admin_cant_change_user_data(admin_client, user_item):
    pk = user_item.pk
    endpoint = f'/users/{pk}/'
    response = admin_client.patch(path=endpoint,
                                  data={"title": "any_title"},
                                  format='json')
    assert response.status_code == 401


def test_admin_can_view_all_pages(admin_client):
    request = '/pages/'
    response = admin_client.get(path=request)
    assert response.status_code == 200


def test_user_can_add_tag(api_auth_client, page_item):
    page_pk = page_item.pk
    tag_name = 'test_tag'
    page = Page.objects.get(pk=page_pk)
    init_len = len(page.tags.all())
    endpoint = f'/pages/{page_pk}/tagCreate/?tag={tag_name}'
    response = api_auth_client.patch(path=endpoint)
    assert response.status_code == 201
    page = Page.objects.get(pk=page_pk)
    final_len = len(page.tags.all())
    assert final_len - init_len == 1


def test_user_can_delete_tag(api_auth_client, page_item):
    page_pk = page_item.pk
    tag_name = 'test_tag'
    endpoint = f'/pages/{page_pk}/tagDelete/?tag={tag_name}'
    response = api_auth_client.patch(path=endpoint)
    assert response.status_code == 202


def test_moderator_can_view_all_pages(moderator_client):
    request = '/pages/'
    response = moderator_client.get(path=request)
    assert response.status_code == 200


def test_moderator_can_block_page(admin_client, page_item):
    pk = page_item.pk
    endpoint = f'/pages/{pk}/blockPage/?hour={1}&min={5}'
    response = admin_client.get(path=endpoint)
    assert response.status_code == 202 


def test_moderator_can_delete_any_post(moderator_client, post_item):
    pk = post_item.pk
    endpoint = f'/posts/{pk}/'
    response = moderator_client.delete(path=endpoint)
    assert response.status_code == 204  #no content


def test_user_can_view_liked_posts(api_auth_client, post_item_with_like):
    endpoint = '/likedPosts'
    response = api_auth_client.get(path=endpoint)
    assert response.status_code == 200



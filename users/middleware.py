import os
import jwt

from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.shortcuts import get_object_or_404

from rest_framework import status

from users.models import User
from users.utils import generate_access_token

from dotenv import load_dotenv
load_dotenv()

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self._exclusion_list = ('/register', '/login')

    def __call__(self, request):
        if request.path not in self._exclusion_list and not request.path.startswith('/admin/'):
            try:
                token = request.headers.get('Authorization')
                if token:
                    decoded = jwt.decode(token, os.getenv('SECRET_KEY', ""), algorithms=['HS256']) 
                    user_id = decoded.get("user_id")
                    request.user = get_object_or_404(User, id=user_id)
                else:
                    raise ImproperlyConfigured(error)
            except (jwt.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidTokenError):
                error = {
                    "error_code": status.HTTP_403_FORBIDDEN,
                    "error_message": "The token is invalid or expired.",
                }
                raise PermissionDenied(error)
        return self.get_response(request)
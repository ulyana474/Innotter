import os
import jwt

from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response

from users.models import User
from users.utils import generate_access_token

from dotenv import load_dotenv
load_dotenv()

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self._exclusion_list = ('/register', '/login/')

    def __call__(self, request):
        if request.path not in self._exclusion_list and not request.path.startswith('/admin/'):
            try:
                token = request.headers.get('Authorization')
                if token:
                    decoded = jwt.decode(token, os.getenv('SECRET_KEY', ""), algorithms=['HS256']) 
                    user_id = decoded.get("user_id")
                    request.user = get_object_or_404(User, id=user_id)
                else:
                    return HttpResponseForbidden("Request doesn't contain Authorization in header")
            except (jwt.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidTokenError):
                return HttpResponseForbidden("Signature expired")
            except (jwt.DecodeError):
                return HttpResponseForbidden("Decode error")
            except (jwt.InvalidTokenError):
                return HttpResponseForbidden("Invalid token")
        return self.get_response(request)
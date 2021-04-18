from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from core import serializers as core_serializers
from django.conf import settings
from core import models as core_models
from helpers import decorators as helper_decorators
from rest_framework import decorators, views, permissions, status
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken

import base64
import jwt

# Create your views here.


@csrf_exempt
@decorators.api_view(["POST"])
@helper_decorators.validate_post_request_body(validator=core_serializers.LoginRequest)
def login(request, *args, **kwargs):
    res = {}
    res_status = status.HTTP_200_OK

    req_json = kwargs.get('req_json')

    user = core_models.User.objects.get(email=req_json.get("email").lower())

    if not user.is_active:
        res_status = status.HTTP_401_UNAUTHORIZED
        res["detail"] = "Sorry! You cannot login, your account has not been approved"
    else:
        user_authentication = authenticate(
            username=user.username, password=req_json.get("password"))

        if user_authentication is not None:
            res["user"] = core_serializers.UserResponse(user).data
            refresh_token = RefreshToken.for_user(user)
            res["refresh_token"] = str(refresh_token)
            res["access_token"] = str(refresh_token.access_token)
        else:
            res["errors"] = {
                "password": ["The provided credentials are wrong"]}
            res_status = status.HTTP_401_UNAUTHORIZED

    return JsonResponse(res, status=res_status)
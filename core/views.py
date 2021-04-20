from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from core import serializers as core_serializers
from django.conf import settings
from core import models as core_models
from helpers import decorators as helper_decorators
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets, mixins, decorators, views, permissions, status, pagination

import base64
import jwt
import json

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

class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'per_page'
    max_page_size = 1000

class DataViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LargeResultsSetPagination
    serializer_class = core_serializers.DataQuickResponse
    paginate_by = 10
    
    queryset = core_models.Data.objects.all()

    def list(self, request):
        user = request.user

        queryset = self.filter_queryset(core_models.Data.objects.filter(
            user_id=user.pk))

        page = request.GET.get('page')
        try:
            page = self.paginate_queryset(queryset)
        except Exception as e:
            page = []
            data = page
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": 'No more record.',
                "data": data
            })

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = serializer.data
            return self.get_paginated_response(data)

        return Response({
            "status": status.HTTP_200_OK,
            "message": 'User Data List',
            "data": data
        })

    def post(self, request):
        res = {}
        res_status = status.HTTP_201_CREATED

        user = request.user

        image_file = request.FILES['file']
        req_data = request.POST.get('data')

        data = core_models.Data()
        data.user_id = user.pk
        data.data = json.loads(req_data)
        data.image = image_file
        data.save()

        res['data'] = core_serializers.DataQuickResponse(data).data
        return JsonResponse(res, status=res_status)

    def retrieve(self, request, pk=None):
        res = {}
        res_status = status.HTTP_200_OK
        
        data = core_models.Data.objects.get(pk=pk)

        selected_serializer = None


        if request.GET.get("extended") is not None and request.GET.get("extended") != "" and json.loads(request.GET.get("extended")):
            selected_serializer = core_serializers.DataFullResponse
        else:
            selected_serializer = core_serializers.DataQuickResponse

        res['data'] =selected_serializer(data).data
        return JsonResponse(res, status=res_status)

@csrf_exempt
@decorators.api_view(["POST"])
def submit_data(request):
    res = {}
    res_status = status.HTTP_201_CREATED

    user = request.user

    image_file = request.FILES['file']
    req_data = request.POST.get('data')

    data = core_models.Data()
    data.user_id = user.pk
    data.data = json.loads(req_data)
    data.image = image_file
    data.save()

    res['data'] = core_serializers.DataQuickResponse(data).data
    return JsonResponse(res, status=res_status)

@decorators.api_view(["GET"])
def get_data(request, pk):
    res = {}
    res_status = status.HTTP_200_OK
    
    data = core_models.Data.objects.get(pk=pk)

    res['data'] = core_serializers.DataQuickResponse(data).data
    return JsonResponse(res, status=res_status)

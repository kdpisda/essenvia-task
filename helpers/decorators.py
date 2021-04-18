from rest_framework import status
from django.http import JsonResponse
from rest_framework import status
import json


def validate_post_request_body(validator=None):
    def decorator(function):
        def wrap(request, *args, **kwargs):
            data = request.body.decode('utf-8')
            res = {}
            req = {}
            try:
                req = json.loads(data)
            except Exception as e:
                res["errors"] = {"body": ["Invalid Request Body"]}
                return JsonResponse(res, status=status.HTTP_400_BAD_REQUEST)
            validation = validator(data=req)
            if not validation.is_valid():
                res["errors"] = validation.errors
                return JsonResponse(res, status=status.HTTP_400_BAD_REQUEST)
            kwargs["req_json"] = req
            return function(request, *args, **kwargs)
        wrap.__doc__ = function.__doc__
        wrap.__name__ = function.__name__
        return wrap
    return decorator


def validate_post_request_body_class_method(validator=None):
    def decorator(function):
        def wrap(self, request, *args, **kwargs):
            res = {}
            # res_status = status.HTTP_200_OK
            # try:
            data = request.body.decode('utf-8')
            req = {}
            try:
                req = json.loads(data)
            except Exception as e:
                res["errors"] = {"body": ["Invalid Request Body"]}
                return JsonResponse(res, status=status.HTTP_400_BAD_REQUEST)
            validation = validator(data=req)
            if not validation.is_valid():
                res["errors"] = validation.errors
                return JsonResponse(res, status=status.HTTP_400_BAD_REQUEST)
            kwargs["req_json"] = req
            return function(self, request, *args, **kwargs)
            # except Exception as error:
            #     res["detail"] = str(error)
            #     res_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            #     return JsonResponse(res, status=res_status)
        wrap.__doc__ = function.__doc__
        wrap.__name__ = function.__name__
        return wrap
    return decorator

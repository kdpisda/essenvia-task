from rest_framework import serializers
from django.contrib.auth.models import User

class LoginRequest(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_null=False)
    password = serializers.CharField(
        required=True, max_length=256, allow_null=False)

    def validate_email(self, value):
        if not User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError(
                "We couldn’t identify you. Please create an account to login!")

class DataSubmitRequest(serializers.Serializer):
    data = serializers.JSONField(required=True, allow_null=False)
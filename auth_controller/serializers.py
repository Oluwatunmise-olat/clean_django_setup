from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

USER = get_user_model()


class UserRegistrationSerializer(ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = USER
        fields = [
            "first_name",
            "last_name",
            "password",
            "email",
            "user_type",
            "created_at",
            "is_active",
        ]
        read_only_fields = ["user_type", "created_at", "is_active"]


class UserLoginSerializer(ModelSerializer):
    class Meta:
        model = USER
        fields = ["email", "password"]

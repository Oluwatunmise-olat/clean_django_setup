from common.enums import UserTypes
from common.response import ResponseInstance
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated

from .serializers import UserLoginSerializer, UserRegistrationSerializer

USER = get_user_model()


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def user_signup(request):
    ser = UserRegistrationSerializer
    request_serializer = ser(data=request.data)

    if not request_serializer.is_valid():
        return ResponseInstance.api_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            has_error=True,
            error_code=1304,
            data=request_serializer.errors,
        )

    user = request_serializer.save(
        password=make_password(request_serializer.validated_data["password"])
    )

    user_data = ser(instance=user)

    return ResponseInstance.api_response(
        status_code=status.HTTP_201_CREATED,
        has_error=False,
        data=user_data.data,
        message="User Created",
    )


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def admin_signup(request):
    ser = UserRegistrationSerializer
    request_serializer = ser(data=request.data)

    if not request_serializer.is_valid():
        return ResponseInstance.api_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            has_error=True,
            error_code=1304,
            data=request_serializer.errors,
        )

    user = request_serializer.save(
        password=make_password(request_serializer.validated_data["password"]),
        user_type=UserTypes["AdminUser"].value,
        is_staff=True,
    )

    user_data = ser(instance=user)

    return ResponseInstance.api_response(
        status_code=status.HTTP_201_CREATED,
        has_error=False,
        data=user_data.data,
        message="User Created",
    )


@api_view(["POST"])
def login(request):
    request_serializer = UserLoginSerializer(data=request.data)
    response_serializer = UserRegistrationSerializer

    if not request_serializer.is_valid():
        return ResponseInstance.api_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            has_error=True,
            error_code=1304,
            data=request_serializer.errors,
        )
    auth_user = authenticate(
        email=request_serializer.validated_data["email"],
        password=request_serializer.validated_data["password"],
    )

    if not auth_user:
        return

    response_data = response_serializer(instance=auth_user).data

    return ResponseInstance.api_response(
        status_code=status.HTTP_200_OK,
        has_error=False,
        message="Login Success",
        data=response_data,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logout(request):
    pass

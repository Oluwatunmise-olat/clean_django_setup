from common.response import ResponseInstance
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated

from .serializers import UserRegistrationSerializer


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def user_signup(request):
    ser = UserRegistrationSerializer
    serialized_request = ser(data=request.data)

    if not serialized_request.is_valid():
        return ResponseInstance.api_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            has_error=True,
            error_code=1304,
            data=serialized_request.errors,
        )

    user = serialized_request.save(
        password=make_password(serialized_request.validated_data["password"])
    )

    user_data = ser(instance=user)

    return ResponseInstance.api_response(
        status_code=status.HTTP_201_CREATED,
        has_error=False,
        data=user_data.data,
        message="User Created",
    )


def admin_signup(request):
    pass


@api_view(["POST"])
def login(request):
    pass


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logout(request):
    pass

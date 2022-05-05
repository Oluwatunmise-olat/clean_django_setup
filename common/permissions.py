from rest_framework import status
from rest_framework.permissions import SAFE_METHODS, BasePermission

from common.enums import UserTypes
from common.response import ResponseInstance


class IsOwnerOrAdmin(BasePermission):
    message = "Unauthorized to Access Resource"

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return (
            True
            if (request.user.is_staff and request.user_type == UserTypes["AdminUser"].value)
            or obj.author == request.user
            else False
        )

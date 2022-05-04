from common.pagination import CustomPagination
from common.permissions import IsOwnerOrAdmin
from common.response import ResponseInstance
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from post_controller import serializers

from .models import Post as PostModel
from .serializers import PostSerializer


class PostRequestView(APIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    pagination_class = CustomPagination
    model = PostModel

    instantiate_paginator = pagination_class()

    def get(self, request, post_id, *args, **params):

        has_instance = self.model.objects.filter(author=request.user, pk=post_id)

        if not has_instance:
            return ResponseInstance.api_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Resource Not Found",
                has_error=True,
                error_code=1103,
            )

        serialized_response = self.serializer_class(instance=has_instance.get()).data

        return ResponseInstance.api_response(
            status_code=status.HTTP_200_OK,
            has_error=False,
            message="Post Created",
            data=serialized_response,
        )

    def post(self, request, *args, **params):
        serialized_request = self.serializer_class(data=request.data)

        if not serialized_request.is_valid():
            return ResponseInstance.api_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                has_error=True,
                error_code=1304,
                data=serialized_request.errors,
            )

        post = serialized_request.save(author=request.user)

        serialized_response = self.serializer_class(instance=post).data

        return ResponseInstance.api_response(
            status_code=status.HTTP_200_OK,
            has_error=False,
            message="Post Created",
            data=serialized_response,
        )

    def patch(self, request, *args, **kwargs):

        serialized_request = self.serializer_class(data=request.data, partial=True)

        if not serialized_request.is_valid():
            return ResponseInstance.api_response(
                has_error=True,
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code=11304,
                data=serialized_request.errors,
            )

        post_instance = self.model.objects.filter(pk=kwargs["post_id"])

        if not post_instance.exists():
            return ResponseInstance.api_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Resource Not Found",
                has_error=True,
                error_code=1103,
            )

        self.check_object_permissions(request, post_instance.get())

        serialized_response = self.serializer_class(
            instance=serialized_request.update(author=request.user, instance=post_instance.get())
        ).data

        return ResponseInstance.api_response(
            has_error=False,
            status_code=status.HTTP_200_OK,
            message="Update SuccessFul",
            data=serialized_response,
        )

    def delete(self, request, *args, **kwargs):
        post_instance = self.model.objects.filter(pk=kwargs["post_id"])

        if not post_instance.exists():
            return ResponseInstance.api_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Resource Not Found",
                has_error=True,
                error_code=1103,
            )

        self.check_object_permissions(request, post_instance.get())

        post_instance.delete()

        return ResponseInstance.api_response(
            has_error=False,
            status_code=status.HTTP_204_NO_CONTENT,
            message="Resource Deleted",
        )

    def get_paginated_queryset(self, model_instances, request_object):

        return self.instantiate_paginator.paginate_queryset(model_instances, request_object)

    def get_paginated_serialized_data(self, serialized_data):
        return self.instantiate_paginator.get_paginated_response(serialized_data)


class PostListView(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    model = PostModel

    def get_queryset(self):
        is_done = self.request.GET.get("done", None)
        params = {"author": self.request.user}

        if not is_done:
            return self.model.objects.filter(**params)
        params["is_done"] = is_done

        return self.model.objects.filter(**params)

    def list(self, request, *args, **kwargs):
        response_data = super().list(request, *args, **kwargs)

        return ResponseInstance.api_response(
            status_code=response_data.status_code,
            has_error=False,
            data=response_data.data,
            message="All Posts Fetched",
        )


@api_view(["POST"])
def upload_post_media(request):
    pass

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, Serializer

from . import models


class PostSerializer(ModelSerializer):
    class Meta:
        model = models.Post
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at", "author"]

    def validate(self, attrs):

        object_id = attrs.get("id", None)
        object_exists = self.Meta.model.objects.filter(pk=object_id)

        if object_id and not object_exists.exists():
            raise ValidationError("Resource Not Found")

        if object_id and object_exists.exists():
            attrs["object_instance"] = object_exists.get()

        return super().validate(attrs)

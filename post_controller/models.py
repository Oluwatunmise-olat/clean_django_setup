from common.models import BaseModel
from django.contrib.auth import get_user_model
from django.db import models

USER = get_user_model()


class Post(BaseModel):

    author = models.ForeignKey(
        to=USER,
        on_delete=models.CASCADE,
        db_column="author_id",
        related_name="users_post",
    )
    title = models.CharField(max_length=120)
    is_done = models.BooleanField(default=False)
    description = models.TextField(null=True)

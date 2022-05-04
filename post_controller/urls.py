from django.urls import path

from . import views

app_name = "post_controller"

urlpatterns = [
    path("create", views.PostRequestView.as_view(), name="create post/todo"),
    path("", views.PostListView.as_view(), name="get all posts"),
    path(
        "<post_id>", views.PostRequestView.as_view(), name="delete/update/get single post endpoint"
    ),
]

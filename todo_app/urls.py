from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("auth/", include("auth_controller.urls", namespace="auth_routes")),
    path("posts/", include("post_controller.urls", namespace="post_routes")),
]

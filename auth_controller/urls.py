from django.urls import path

app_name = "auth"

from . import views

urlpatterns = [
    path("signup", views.user_signup, name="user signup"),
]

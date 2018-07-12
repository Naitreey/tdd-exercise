from django.urls import path

from . import views


app_name = "accounts"

urlpatterns = [
    path(
        "login/",
        views.LoginView.as_view(),
        name="login",
    ),
    path(
        "login/<uidb64>/<token>/",
        views.LoginConfirmView.as_view(),
        name="login-confirm",
    ),
]

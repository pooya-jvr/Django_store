from django.urls import path, include
from . import views


app_name = "accounts"

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="user_register"),
    path("verify/", views.UserRegisterVerifyCodeView.as_view(), name="verify_code"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]

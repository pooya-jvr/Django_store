from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, VerifyCodeForm, UserLoginForm
import random
from utils import send_otp_code
from .models import User, OtpCode
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate, login, logout


class UserRegisterView(View):
    form_class = UserRegistrationForm

    def get(self, request):
        form = self.form_class
        return render(request, "accounts/register.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            random_code = random.randrange(1000, 9999)
            send_otp_code(form.cleaned_data["phone"], random_code)
            OtpCode.objects.create(
                phone_number=form.cleaned_data["phone"], code=random_code
            )
            request.session["user_registertion_info"] = {
                "phone_number": form.cleaned_data["phone"],
                "email": form.cleaned_data["email"],
                "full_name": form.cleaned_data["full_name"],
                "password": form.cleaned_data["password"],
            }
            messages.success(request, "we send you a code", "success")
            return redirect("accounts:verify_code")

        return render(request, "accounts/register.html", {"form": form})


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, "accounts/verify.html", {"form": form})

    def post(self, request):
        user_session = request.session["user_registertion_info"]
        code_istance = OtpCode.objects.get(phone_number=user_session["phone_number"])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd["code"] == code_istance.code:
                User.objects.create_user(
                    user_session["phone_number"],
                    user_session["email"],
                    user_session["full_name"],
                    user_session["password"],
                )

                code_istance.delete()
                messages.success(request, "you registred.", "success")
                return redirect("home:home")

            else:
                messages.error(request, "this code is wrong", "danger")
                return redirect("accounts:verify_code")
        return redirect("home:home")


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "ypu logged out successfully", "success")
        return redirect("home:home")


class LoginView(View):
    form_class = UserLoginForm
    template_name = "accounts/login.html"

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, phone_number=cd["phone_number"], password=cd["password"]
            )
            if user is not None:
                login(request, user)
                messages.success(request, "you logged in successfully", "info")
                return redirect("home:home")
            messages.error(request, "phone number or password is wrong", "warning")
        return render(request, self.template_name, {"form": form})

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login

from . import forms


class LoginView(FormView):

    template_name = "accounts/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("accounts:login-sent")

    def form_valid(self, form):
        form.save()
        return super().form_valid()


class LoginConfirmView(View):

    login_error_template = "accounts/login_error.html"

    def get(self, request, uidb64, token, *args, **kwargs):
        user = authenticate(request, uidb64=uidb64, token=token)
        if user is None:
            return render(request, self.login_error_template)
        login(request, user)
        return redirect("home")


class LoginSentView(View):
    pass

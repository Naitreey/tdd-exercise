import http

from django.shortcuts import render, redirect
from django.views.generic import View, FormView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views

from todo import forms as todo_forms
from . import forms


class LoginView(SuccessMessageMixin, FormView):

    form_class = forms.LoginForm
    success_url = reverse_lazy("home")
    template_name = "todo/index.html"
    success_message = "Login email has been sent."

    def form_valid(self, form):
        form.save(
            scheme=self.request.scheme,
            domain=self.request.get_host()
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        if "form" in kwargs:
            kwargs['form'], kwargs['loginform'] \
                = todo_forms.NewListForm(), kwargs['form']
        return super().get_context_data(**kwargs)


class LoginConfirmView(View):

    invalid_login_template_name = "accounts/login_invalid.html"

    def get(self, request, uidb64, token):
        user = authenticate(request, uidb64=uidb64, token=token)
        if user is None:
            return render(
                request, 
                self.invalid_login_template_name, 
                status=http.HTTPStatus.NOT_FOUND.value,
            )
        else:
            login(request, user)
            return redirect("home")


class LogoutView(auth_views.LogoutView):

    next_page = "home"

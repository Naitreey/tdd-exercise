from django.shortcuts import render
from django.views.generic import View, FormView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

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
                = todo_forms.NewListItemForm(), kwargs['form']
        return super().get_context_data(**kwargs)

class LoginConfirmView(View):
    pass

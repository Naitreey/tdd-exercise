from django import forms
from django.contrib.auth import get_user_model

from . import models


class LoginForm(forms.Form):

    email = get_user_model()._meta.get_field("email").formfield()

    def save(self, uidb64, token,
             subject_template_name="accounts/"
             email_template_name="accounts/login_email_template.html"):

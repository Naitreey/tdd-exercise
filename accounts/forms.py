from urllib.parse import urlunsplit

from django import forms
from django.contrib.auth import get_user_model
from django.core import mail
from django.template import loader
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.utils.encoding import force_bytes
from django.core.exceptions import ValidationError
from django.urls import reverse


UserModel = get_user_model()


class LoginForm(forms.Form):

    email = UserModel._meta.get_field("email").formfield(
        error_messages={
            "required": "Email can not be empty",
        },
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            raise ValidationError(
                message="The account is unregistered.",
                code="unknown",
            )
        else:
            return email

    def save(self, scheme, domain,
             subject_template_name="accounts/login_email_subject.txt",
             email_template_name="accounts/login_email_template.html"):
        if self.errors:
            raise ValueError(
                "Email can not be sent, because login form didn't validate."
            )
        sender = settings.LOGIN_SENDER_EMAIL
        email = self.cleaned_data['email']
        user = UserModel.objects.get_by_natural_key(email)
        login_url = reverse(
            "accounts:login-confirm",
            kwargs={
                "uidb64": urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                "token": default_token_generator.make_token(user),
            }
        )
        subject = loader.render_to_string(subject_template_name).strip()
        message = loader.render_to_string(
            email_template_name,
            context={
                "login_url": urlunsplit((scheme, domain, login_url, "", ""))
            },
        )
        mail.send_mail(subject, message, sender, [email])

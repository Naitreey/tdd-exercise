from django import forms
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string


class LoginForm(forms.Form):

    email = get_user_model()._meta.get_field("email").formfield()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean_email(self):
        UserModel = get_user_model()
        email = self.cleaned_data['email']
        message = "Invalid email address."
        try:
            self.user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            raise ValidationError(message=message, code="invalid")
        else:
            return email

    def save(self, uidb64, token,
             subject="registration/login_email_subject.txt",
             email_template_name="registration/login_email_message.html"):
        pass

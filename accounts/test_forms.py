from django.test import TestCase

from .. import forms


class LoginFormTest(TestCase):

    def test_can_not_enter_empty_email(self):
        form = forms.LoginForm(data={"email": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("Email can not be empty", form.errors['email'])

    def test_can_not_enter_invalid_email(self):
        email = "abc"
        form = forms.LoginForm(data={"email": email})
        self.assertFalse(form.is_valid())
        self.assertIn(f"Enter a valid email address.", form.errors['email'])

    def test_can_enter_valid_email(self):
        email = "test@gmail.com"
        form = forms.LoginForm(data={"email": email})
        self.assertTrue(form.is_valid())

    def test_will_send_email_on_submit(self):
        email = "test@gmail.com"
        form = forms.LoginForm(data={"email": email})
        form.save()

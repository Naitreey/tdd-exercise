from unittest.mock import Mock, patch

import django
from django.test import TestCase
from django.core.exceptions import ValidationError

from .. import forms, models


class LoginFormTest(TestCase):

    registered_email = "test@gmail.com"

    def setUp(self):
        models.User.objects.create_user(email=self.registered_email)

    def test_can_not_enter_empty_email(self):
        form = forms.LoginForm(data={"email": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("Email can not be empty", form.errors['email'])

    def test_can_not_enter_invalid_email(self):
        email = "abc"
        form = forms.LoginForm(data={"email": email})
        self.assertFalse(form.is_valid())
        self.assertIn(f"Enter a valid email address.", form.errors['email'])

    def test_can_not_enter_unregistered(self):
        email = "a@se.com"
        form = forms.LoginForm(data={"email": email})
        self.assertFalse(form.is_valid())
        self.assertIn("The account is unregistered.", form.errors['email'])

    def test_can_enter_registered_email(self):
        form = forms.LoginForm(data={"email": self.registered_email})
        self.assertTrue(form.is_valid())

    def test_raise_error_on_invalid_email(self):
        email = "abc"
        form = forms.LoginForm(data={"email": email})
        with self.assertRaises(ValueError):
            form.save("http", "localhost")

    def test_raise_error_if_unregistered(self):
        form = forms.LoginForm(data={"email": "a@b.c"})
        with self.assertRaises(ValueError):
            form.save("http", "localhost")

    @patch("django.core.mail.send_mail")
    def test_send_email_if_registered(self, send_mail):
        email = self.registered_email
        form = forms.LoginForm(data={"email": email})
        form.save("http", "localhost")
        (subject, message, from_email, recipient_list, *rest), kwargs = \
            send_mail.call_args
        self.assertTrue(send_mail.called)
        self.assertEqual(
            from_email,
            django.conf.settings.LOGIN_SENDER_EMAIL,
        )
        self.assertEqual(recipient_list[0], email)
        self.assertEqual(subject, "Your login url to To-Do List site")
        self.assertInHTML(
            "Click the following url to log in to To-Do list site:",
            message,
        )
        self.assertRegex(message, r"http://.*/accounts/login/.*/.*/")

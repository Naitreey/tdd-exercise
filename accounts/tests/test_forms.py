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
            form.save()

    def test_raise_error_if_unregistered(self):
        form = forms.LoginForm(data={"email": "a@b.c"})
        with self.assertRaises(ValueError):
            form.save()

    def test_send_email_if_registered(self):
        email = self.registered_email

        # mock by monkeypatching
        django.core.mail.send_mail = self.fake_send_mail

        form = forms.LoginForm(data={"email": email})
        form.save()

        self.assertTrue(self.fake_send_mail_called)
        self.assertEqual(
            self.fake_send_mail_from_email,
            django.conf.settings.LOGIN_SENDER_EMAIL,
        )
        self.assertEqual(self.fake_send_mail_recipient_list[0], email)
        self.assertEqual(
            self.fake_send_mail_subject,
            "Your login url to To-Do List site",
        )
        self.assertRegex(
            self.fake_send_mail_message,
            "Click the following url to log in to To-Do list site:",
        )

    def fake_send_mail(self, subject, message, from_email, recipient_list,
                       fail_silently=False, auth_user=None, auth_password=None,
                       connection=None, html_message=None):
        self.fake_send_mail_called = True
        self.fake_send_mail_subject = subject
        self.fake_send_mail_message = message
        self.fake_send_mail_from_email = from_email
        self.fake_send_mail_recipient_list = recipient_list
        self.fake_send_mail_fail_silently = fail_silently
        self.fake_send_mail_auth_user = auth_user
        self.fake_send_mail_auth_password = auth_password
        self.fake_send_mail_connection = connection
        self.fake_send_mail_html_message = html_message
        return len(recipient_list)

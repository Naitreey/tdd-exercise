import django
from django.test import TestCase

from todo import forms as todo_forms
from .. import models, forms


class LoginViewTest(TestCase):

    email = "abc@test.com"

    def setUp(self):
        models.User.objects.create_user(email=self.email)

    def test_homepage_has_loginform_if_not_logged_in(self):
        response = self.client.get("/")
        self.assertIsInstance(response.context['loginform'], forms.LoginForm)

    def test_sent_email_alert_if_login_success(self):
        response = self.login(email=self.email, follow=True)
        self.assertEqual(len(response.context['messages']), 1)
        self.assertEqual(
            list(response.context['messages'])[0].message,
            "Login email has been sent."
        )
        self.assertContains(response, "Login email has been sent.")

    def test_failed_login_context_forms(self):
        response = self.login(email="test@test.com")
        self.assertIsInstance(
            response.context['form'],
            todo_forms.NewListItemForm,
        )
        self.assertIsInstance(
            response.context['loginform'],
            forms.LoginForm,
        )

    def test_unregistered_can_not_login(self):
        response = self.login(email="test@test.com")
        self.assertContains(response, "The account is unregistered.")

    def test_empty_email_can_not_login(self):
        response = self.login(email="")
        self.assertContains(response, "Email can not be empty")

    def login(self, email, follow=False):
        return self.client.post(
            "/accounts/login/",
            data={"email": email},
            follow=follow,
        )

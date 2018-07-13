import django
from django.test import TestCase

from todo import forms as todo_forms
from .. import models, forms


class BaseAccountViewTest(TestCase):

    email = "abc@test.com"

    def setUp(self):
        user = models.User.objects.create_user(email=self.email)
        self.uidb64 = user.uidb64
        self.token = user.make_auth_token()

    def login(self, email, follow=False):
        return self.client.post(
            "/accounts/login/",
            data={"email": email},
            follow=follow,
        )

    def login_confirm(self, follow=False):
        return self.client.get(
            f"/accounts/login/{self.uidb64.decode()}/{self.token}/",
            follow=follow,
        )


class LoginViewTest(BaseAccountViewTest):

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


class LoginConfirmViewTest(BaseAccountViewTest):

    def test_redirect_to_homepage_if_logged_in(self):
        response = self.login_confirm()
        self.assertRedirects(response, "/")

    def test_navbar_login_status_if_logged_in(self):
        response = self.login_confirm(follow=True)
        self.assertContains(
            response,
            f"You have logged in as {self.email}.",
        )

    def test_invalid_credentials_can_not_login(self):
        response = self.client.get("/accounts/login/sef/sef/")
        self.assertContains(
            response,
            "Your login link is invalid.",
            status_code=404,
        )

    def test_a_url_can_be_used_only_once(self):
        response = self.login_confirm()
        response = self.login_confirm()
        self.assertContains(
            response,
            "Your login link is invalid.",
            status_code=404,
        )


class LogoutViewTest(BaseAccountViewTest):

    def test_can_logout_when_logged_in(self):
        self.login_confirm()
        response = self.logout(follow=True)
        self.assertContains(response, "Log In")

    def test_can_logout_when_not_logged_in(self):
        response = self.logout(follow=True)
        self.assertContains(response, "Log In")

    def logout(self, follow=False):
        return self.client.post("/accounts/logout/", follow=follow)

from django.test import TestCase


class LoginViewTest(TestCase):

    def test_redirect_to_homepage_if_login_success(self):
        email = "abc@test.com"
        response = self.client.post("/accounts/login/", data={"email": email})
        self.assertRedirects(response, "/")

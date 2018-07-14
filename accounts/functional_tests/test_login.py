from xml.etree import ElementTree as ET

from selenium.common.exceptions import WebDriverException

from django.core import mail
from django.contrib.auth import get_user_model

from todo.functional_tests.base import EmptyInputTestMixin, ToDoListTest

class LoginTest(ToDoListTest):

    registered_email = "test@test.test"

    def setUp(self):
        get_user_model().objects.create_user(email=self.registered_email)

    def test_user_can_login(self):
        login_form_selector = "#login-form"
        user_tip = "#nav .tip"
        test_email = self.registered_email

        # Spock visited homepage again
        self.get_homepage()

        # he saw a top bar telling him he can log in
        self.wait_for_elem(login_form_selector)
        self.assertEqual(
            self.find_element("#nav button").text,
            "Log In",
        )

        # we now logs into site by typing his celestial mail address
        self.check_and_input_text(
            f"{login_form_selector} input[name=email]",
            test_email,
        )

        # and pressed login button
        self.find_element(
            f'{login_form_selector} button[type="submit"]'
        ).click()

        # the page refreshed. A banner message told him the login url has been
        # sent as an email message, please check it out
        self.wait_for_fn(
            lambda: self.assertEqual(
                self.find_element(".login-alert").text,
                "Login email has been sent.",
            )
        )

        # he saw it in mail box
        ## in unit test we use django mail.outbox to mock external
        ## mail service
        message = mail.outbox[0]
        self.assertSetEqual({*message.to}, {test_email})

        # the email's title says Your login url to To-Do List site.
        self.assertEqual(
            message.subject,
            "Your login url to To-Do List site",
        )

        # the email's content says Click the following url to log in
        # to To-Do list site:
        self.assertRegex(
            message.body,
            "Click the following url to log in to To-Do list site:",
        )

        # clicked the url
        root = ET.fromstring(message.body)
        link = root.find(".//a[@id='login']")
        self.browser.get(link.get("href"))

        # now he's redirected back to homepage
        self.wait_for_fn(
            lambda: self.assertEqual(
                self.browser.current_url,
                f"{self.live_server_url}/",
            )
        )

        # the page told him he had logged in.
        self.assertEqual(
            self.wait_for_elem(user_tip).text,
            f"You have logged in as {test_email}.",
        )

        # and login form is now gone.
        with self.assertRaisesRegex(
                WebDriverException, "no such element") as cm:
            self.find_element(login_form_selector)

        # there is a button to logout
        logout_btn = self.find_element("#logout-form button")
        self.assertEqual(logout_btn.text, "Log Out")

        # he clicked button to logout
        logout_btn.click()

        # he now logged out, and has been redirected to homepage with login
        self.wait_for_fn(
            lambda: self.assertEqual(
                self.find_element("#nav button").text,
                "Log In",
            )
        )
        
        # satisfied, Spock returned to Vulcan.

    def get_homepage(self):
        return self.browser.get(self.live_server_url)

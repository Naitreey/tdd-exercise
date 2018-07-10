"""
Tests on homepage.
"""
from xml.etree import ElementTree as ET

from selenium.common.exceptions import WebDriverException

from django.core import mail

from .base import ToDoListTest, EmptyInputTestMixin


class HomePageTest(EmptyInputTestMixin, ToDoListTest):

    def test_can_start_a_new_list(self):
        # Spock opens the homepage of the app, which is http://localhost:8000.
        self.get_homepage()

        # He sees the tab bar have a title named to-do list.
        self.assertIn("To-Do", self.browser.title)

        # homepage's the input box is centered
        self.check_inputbox_centered()

        # He is invited to create a todo list right away by just entering
        # items. He input "do laundary." and press "enter".
        self.assertIn(
            "Start a New To-Do List",
            self.browser.find_element_by_tag_name("h1").text
        )
        todo_text1 = "do laundary"
        self.input_new_todo_item(todo_text1)

        # The page refreshes, Now a new list is created containing the "do
        # laundary" item.
        self.assertIn(
            "Your To-Do List",
            self.browser.find_element_by_tag_name("h1").text
        )
        self.check_todo_list([todo_text1])

        # list page's the input box is centered
        self.check_inputbox_centered()

        # He entered another item "listen online courses."
        todo_text2 = "listen online courses."
        self.input_new_todo_item(todo_text2)

        # The page refreshes, Now the list containing two items.
        self.check_todo_list([todo_text1, todo_text2])

        # satisfied, Spock returned to Vulcan.

    def test_user_can_login(self):
        login_form_selector = "#login-form"
        login_tip = "#nav p.tip"
        test_email = "test@test.test"

        # Spock visited homepage again
        self.get_homepage()

        # he saw a top bar telling him he can log in
        self.wait_for_elem(login_form_selector)
        self.assertEqual(
            self.find_element(login_tip).text,
            "Enter your email address to log in.",
        )

        # we now logs into site by typing his celestial mail address
        self.check_and_input_text(
            f"{login_form_selector} input",
            test_email,
        )

        # and pressed login button
        self.find_element(
            f'{login_form_selector} button[type="submit"]'
        ).click()

        # the page refreshed and told him the login url has been
        # sent as an email message, please check it out
        self.wait_for_fn(
            lambda: self.assertEqual(
                self.find_element(login_tip).text,
                "Login email has been sent.",
            )
        )

        # he saw it in mail box
        ## in unit test we use django mail.outbox to mock external
        ## mail service
        message = mail.outbox[0]
        self.assertSetEqual({message.to}, {test_email})

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
        tree = ET.parse(message.body)
        link = tree.getroot().find(".//a[@id='login']")
        self.browser.get(link.get("href"))

        # now he's redirected back to homepage
        self.wait_for_fn(
            lambda: self.assertEqual(
                self.browser.current_url,
                self.live_server_url,
            )
        )

        # the page told him he had logged in.
        self.asesrtEqual(
            self.wait_for_elem(login_tip).text,
            f"You have logged in as {test_email}.",
        )

        # and login form is now gone.
        with self.assertRaisesRegex(
                WebDriverException, "element not found") as cm:
            self.find_element(login_form_selector)

        # there is a button to logout
        self.assertEqual(self.find_element("#logout").text, "Log out")

        # satisfied, Spock returned to Vulcan.

    def get_homepage(self):
        return self.browser.get(self.live_server_url)

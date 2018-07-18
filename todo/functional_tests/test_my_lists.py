from unittest import skip

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from django.contrib.auth import get_user_model

from .base import ToDoListTest, SessionTestMixin


class MyListsTest(SessionTestMixin, ToDoListTest):

    email = "test@gmail.com"

    def setUp(self):
        self.user = get_user_model().objects.create_user(self.email)

    def test_new_list_is_saved_in_my_lists(self):
        content1 = "what the"
        content2 = "fuck you"
        # the user is authenticated
        self.create_authed_session(self.email)
        # she went to homepage and added to entries
        self.browser.get(self.live_server_url)
        self.input_new_todo_item(content1)
        self.input_new_todo_item(content2)
        ## save current url for comparsion
        current_url = self.browser.current_url
        # she saw there's a "My Lists" link on the page and clicked
        self.wait_for_elem("My Lists", By.LINK_TEXT).click()
        # the page refreshed and she saw her lists are there
        # then she clicked the list back
        self.wait_for_elem(content1, By.LINK_TEXT).click()
        # now she got back to the list she started with.
        self.wait_for_fn(
            lambda: self.assertEqual(self.browser.current_url, current_url)
        )
        # she started another list
        self.browser.get(self.live_server_url)
        content3 = "sef sef esf "
        content4 = "sefse es esf es"
        self.input_new_todo_item(content3)
        self.input_new_todo_item(content4)
        self.wait_for_elem("My Lists", By.LINK_TEXT).click()
        # she saw two lists are shown here
        self.wait_for_elem(content1, By.LINK_TEXT)
        self.wait_for_elem(content3, By.LINK_TEXT)
        # she logged out, seeing no "My Lists" link is shown anymore
        self.find_element("#logout-form button").click()
        with self.assertRaises(NoSuchElementException):
            self.find_element("My Lists", By.LINK_TEXT)

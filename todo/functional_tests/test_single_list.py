"""
Tests on a single list.
"""
from urllib.parse import urljoin

from .base import ToDoListTest, EmptyInputTestMixin
from .. import models


class SingleListTest(EmptyInputTestMixin, ToDoListTest):

    def setUp(self):
        super().setUp()
        self.todolist = models.List.objects.create()
        models.Item.objects.bulk_create([
            models.Item(content="sef", list=self.todolist),
            models.Item(content="seff", list=self.todolist),
        ])

    def test_style_is_loaded(self):
        self.get_list_page()
        self.check_inputbox_centered()

    def test_can_add_item(self):
        # Spock visited his list
        self.get_list_page()
        # trying to add another todo entry
        todo_text1 = "do laundary"
        self.input_new_todo_item(todo_text1)
        # he saw now it's three entries on the list
        self.check_todo_list(["sef", "seff", todo_text1])

    def test_can_not_add_dup_item(self):
        # Spock visited his list
        self.get_list_page()

        # he tried to enter the same entry as before
        text = "sef"
        self.input_new_todo_item(text)

        # but the page tells him that's not possible
        self.check_input_error(
            f'"{text}" already exists, please enter something else.'
        )

        # and it highlighted the duplicated item
        entry = self.browser.find_element_by_css_selector("li.duplicate")
        self.assertRegex(
            entry.text, rf"\d+\. {text}",
            msg='The highlighted item does not match "X. XXX" form.',
        )

        # now he tried to enter a different one
        text = "something else"
        self.input_new_todo_item(text)

        # and it succeeded
        self.check_todo_list(["sef", "seff", text])

    def test_input_error_hide_on_input(self):
        # Spock visited his list
        self.get_list_page()

        # he tried to enter the same entry as before
        text = "sef"
        self.input_new_todo_item(text)

        # but the page tells him that's not possible
        self.check_input_error(
            f'"{text}" already exists, please enter something else.'
        )
        self.assertTrue(
            self.get_input_error_element().is_displayed()
        )

        # he focused on input bar and start to try again,
        # the input error disappeared
        self.check_and_input_text(self.input_selector, "x")
        self.assertFalse(
            self.get_input_error_element().is_displayed()
        )

    def get_list_page(self):
        self.browser.get(
            urljoin(self.live_server_url, f"lists/{self.todolist.pk}/")
        )

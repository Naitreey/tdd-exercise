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
        self.browser.get(
            urljoin(self.live_server_url, f"lists/{self.todolist.pk}/")
        )
        self.check_inputbox_centered()

    def test_can_add_item(self):
        # Spock visited his list
        self.browser.get(
            urljoin(self.live_server_url, f"lists/{self.todolist.pk}/")
        )
        # trying to add another todo entry
        todo_text1 = "do laundary"
        self.input_new_todo_item(todo_text1)
        # he saw now it's three entries on the list
        self.check_todo_list(["sef", "seff", todo_text1])

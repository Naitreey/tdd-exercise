"""
Tests on a set of lists.
"""
from urllib.parse import urljoin

from .base import ToDoListTest


class ListsTest(ToDoListTest):

    def test_lists_have_unique_urls(self):
        # Spock opened the page
        self.browser.get(self.live_server_url)

        # entered a new todo entry
        todo_text = "do laundary"
        self.input_new_todo_item(todo_text)

        # noticed that a new list is created and has a unique url
        self.check_todo_list([todo_text])
        spock_list_url = self.browser.current_url
        self.assertRegex(
            spock_list_url,
            urljoin(f"{self.live_server_url}", r"lists/.+/")
        )

        # another user Kirk opened the page
        self.browser.get(self.live_server_url)

        # now the todo list is empty
        todos = self.browser.find_elements_by_tag_name("li")
        self.assertEqual(len(todos), 0)

        # Kirk inputs an entry
        todo_text = "some thing"
        self.input_new_todo_item(todo_text)

        # noticed that a new list is created and has a unique url
        self.check_todo_list([todo_text])
        kirk_list_url = self.browser.current_url
        self.assertRegex(
            kirk_list_url,
            urljoin(f"{self.live_server_url}", r"lists/.+/")
        )

        # their todo lists are unqiue
        self.assertNotEqual(spock_list_url, kirk_list_url)

        # satisfied, Kirk go back to Earth.

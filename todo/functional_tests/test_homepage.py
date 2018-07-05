"""
Tests on homepage.
"""
from .base import ToDoListTest, EmptyInputTestMixin


class HomePageTest(EmptyInputTestMixin, ToDoListTest):

    def test_can_start_a_new_list(self):

        # Spock opens the homepage of the app, which is http://localhost:8000.
        self.browser.get(self.live_server_url)

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

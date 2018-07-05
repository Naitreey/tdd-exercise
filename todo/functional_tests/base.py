"""
Base test cases.
"""
import time
from unittest import skip

import numpy as np

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

from django.contrib.staticfiles.testing import StaticLiveServerTestCase


_BROWSER = None


class BaseBrowserTest(StaticLiveServerTestCase):

    max_polling = 10
    polling_interval = 0.1

    @property
    def browser(self):
        global _BROWSER
        if _BROWSER is None:
            _BROWSER = webdriver.Chrome()
        return _BROWSER

    #def setUp(self):
    #    self.browser = webdriver.Chrome()

    #def tearDown(self):
    #    self.browser.quit()

    def check_and_input(self, selector, content, *, placeholder=None):
        elem = self.wait_for(selector)
        if placeholder is not None:
            self.assertEqual(
                elem.get_attribute("placeholder"),
                placeholder,
            )
        elem.send_keys(content)
        elem.send_keys(Keys.ENTER)

    def check_list(self, selector, contents):
        elem = self.wait_for(selector)
        entries = elem.find_elements_by_tag_name("li")
        self.assertEqual(len(contents), len(entries))
        for content, entry in zip(contents, entries):
            self.assertEqual(content, entry.text)

    def wait_for_fn(self, fn, args=None, kwargs=None):
        for _ in np.arange(0, self.max_polling, self.polling_interval):
            try:
                return fn(*(args or []), **(kwargs or {}))
            except (AssertionError, WebDriverException) as e:
                exc = e
                time.sleep(self.polling_interval)
        else:
            raise exc

    def wait_for(self, selector):
        return self.wait_for_fn(
            lambda: self.browser.find_element_by_css_selector(selector)
        )

    wait_for_elem = wait_for


class ToDoListTest(BaseBrowserTest):

    def input_new_todo_item(self, content):
        self.check_and_input(
            "#id_content", content,
            placeholder="Enter a to-do item"
        )

    def check_todo_list(self, items):
        self.check_list(
            "#todo-list",
            [f"{i}. {item}" for i, item in enumerate(items, start=1)],
        )

    def check_inputbox_centered(self):
        size = self.browser.get_window_size()
        input_box = self.wait_for("#id_content")
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width']/2,
            size['width']/2,
            delta=50,
        )


class EmptyInputTestMixin:

    def test_can_not_input_empty_item(self):
        # Spock came back, opened the homepage
        self.browser.get(self.live_server_url)

        # he tried to input an empty item
        self.input_new_todo_item("")

        # but the page tells him "todo entry can not be empty"
        self.check_input_error("To-Do entry can not be empty.")

        # he then input something as todo entry
        self.input_new_todo_item("something")
        self.check_todo_list(["something"])

        # then tried to input an empty item
        self.input_new_todo_item("")

        # the page tells him again "todo entry can not be empty"
        self.check_input_error("To-Do entry can not be empty.")

        # he then input something as todo entry
        self.input_new_todo_item("something else")
        self.check_todo_list(["something", "something else"])

    def check_input_error(self, err_msg):
        error_elem = self.wait_for("#id_content-error")
        self.assertIn(err_msg, error_elem.text)

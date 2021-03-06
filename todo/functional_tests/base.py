"""
Base test cases.
"""
import time
import os
from unittest import skip
from importlib import import_module
from urllib.parse import urljoin

import numpy as np

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import (SESSION_KEY, BACKEND_SESSION_KEY,
                                 HASH_SESSION_KEY, get_user_model)

from todo.utils.test import get_browser_driver


class BaseBrowserTest(StaticLiveServerTestCase):

    max_polling = 10
    polling_interval = 0.1

    @property
    def browser(self):
        return get_browser_driver()

    def check_and_input(self, selector, content, *, placeholder=None):
        elem = self.wait_for(selector)
        if placeholder is not None:
            self.assertEqual(
                elem.get_attribute("placeholder"),
                placeholder,
            )
        elem.send_keys(content)
        elem.send_keys(Keys.ENTER)

    check_and_submit = check_and_input

    def check_and_input_text(self, selector, content):
        elem = self.wait_for_elem(selector)
        elem.send_keys(content)

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

    def wait_for(self, value, by=By.CSS_SELECTOR):
        return self.wait_for_fn(
            lambda: self.find_element(value, by=by)
        )

    def find_element(self, value, by=By.CSS_SELECTOR):
        return self.browser.find_element(by, value)

    wait_for_elem = wait_for


class ToDoListTest(BaseBrowserTest):

    input_selector = "#id_content"
    input_error_selector = f"{input_selector}-error"

    def input_new_todo_item(self, content):
        self.check_and_input(
            self.input_selector, content,
            placeholder="Enter a to-do item"
        )

    def get_input_error_element(self):
        return self.wait_for(self.input_error_selector)

    def check_todo_list(self, items):
        self.check_list(
            "#todo-list",
            [f"{i}. {item}" for i, item in enumerate(items, start=1)],
        )

    def check_inputbox_centered(self):
        size = self.browser.get_window_size()
        input_box = self.wait_for(self.input_selector)
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width']/2,
            size['width']/2,
            delta=50,
        )

    def check_input_error(self, err_msg):
        error_elem = self.get_input_error_element()
        self.assertIn(
            err_msg, error_elem.text,
            msg="The specified input error message is not shown.",
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


class SessionTestMixin:

    def create_authed_session(self, email):
        user = get_user_model().objects.get_by_natural_key(email)
        engine = import_module(settings.SESSION_ENGINE)
        session = engine.SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session[HASH_SESSION_KEY] = user.get_session_auth_hash()
        session.save()
        self.browser.get(urljoin(self.live_server_url, "/sefsef/"))
        self.browser.add_cookie({
            "name": settings.SESSION_COOKIE_NAME,
            "value": session.session_key,
            "path": "/",
        })

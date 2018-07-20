from unittest.mock import patch, Mock

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from .. import forms, models


@patch("todo.models.List")
class NewListFormTest(TestCase):

    def test_create_new_list_with_item(self, MockList):
        text = "sef"
        form = forms.NewListForm(data={"content": text})
        form.save() # should not raise
        MockList.objects.create_new.assert_called_once_with(
            first_item=text, user=None,
        )

    def test_not_create_new_list_with_empty_item(self, MockList):
        content = ""
        form = forms.NewListForm(data={"content": content})
        with self.assertRaisesRegex(
                ValueError, r"the data didn't validate",
                msg="An empty item is erroneously saved."
        ) as cm:
            form.save()
        self.assertIn("To-Do entry can not be empty.", form.errors['content'])

    def test_create_list_with_user_if_logged_in(self, MockList):
        text = "sef"
        user = get_user_model().objects.create_user(email="test@gmail.com")
        form = forms.NewListForm(data={"content": text})
        form.save(user=user)
        MockList.objects.create_new.assert_called_once_with(
            first_item=text,
            user=user,
        )


class ExistingListItemFormTest(TestCase):

    orig_content = "sef"

    def setUp(self):
        self.todolist = models.List.objects.create()
        models.Item.objects.create(
            content=self.orig_content,
            list=self.todolist,
        )

    def test_can_save_different_item(self):
        new_content = "eee"
        form = forms.ExistingListItemForm(
            data={"content": new_content},
            list=self.todolist,
        )
        self.assertTrue(form.is_valid())
        form.save() # do not raise ValueError
        self.assertEqual(self.todolist.entries.count(), 2)
        self.assertEqual(
            self.todolist.entries.filter(
                content=new_content
            ).count(), 1,
        )

    def test_can_not_save_same_item(self):
        form = forms.ExistingListItemForm(
            data={"content": self.orig_content},
            list=self.todolist,
        )
        self.assertFalse(form.is_valid())
        self.assertIn(
            f'"{self.orig_content}" already exists, please enter '
            'something else.',
            form.errors['content'],
        )
        self.assertIsInstance(form.duplicate, models.Item)

    def test_can_not_save_empty_item(self):
        content = ""
        form = forms.ExistingListItemForm(
            data={"content": content},
            list=self.todolist,
        )
        self.assertFalse(form.is_valid())
        self.assertIn(
            "To-Do entry can not be empty.",
            form.errors['content']
        )

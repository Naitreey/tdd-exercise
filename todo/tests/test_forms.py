from django.test import TestCase
from django.core.exceptions import ValidationError

from .. import forms, models


class NewListItemFormTest(TestCase):

    def test_can_save_item(self):
        content = "somtehing"
        list = models.List.objects.create()
        form = forms.NewListItemForm(data={"content": content})
        form.save(list=list)
        self.assertEqual(list.entries.count(), 1)
        self.assertEqual(list.entries.first().content, content)

    def test_can_not_save_empty_item(self):
        content = ""
        list = models.List.objects.create()
        form = forms.NewListItemForm(data={"content": content})
        with self.assertRaisesRegex(
                ValueError, r"the data didn't validate",
                msg="An empty item is erroneously saved."
        ) as cm:
            form.save(list=list)
        self.assertIn("To-Do entry can not be empty.", form.errors['content'])


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

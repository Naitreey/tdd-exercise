from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.exceptions import NON_FIELD_ERRORS
from django.contrib.auth import get_user_model

from .. import models


class ItemModelTest(TestCase):

    def test_item_belongs_to_list(self):
        todo_list = models.List.objects.create()
        item1_text = "new item1"
        item1 = models.Item(
            content=item1_text,
            create_time=timezone.now(),
            list=todo_list,
        )
        item1.save()
        self.assertEqual(
            item1,
            todo_list.entries.get()
        )

    def test_item_can_not_be_empty(self):
        todo_list = models.List.objects.create()
        with self.assertRaises(
                ValidationError,
                msg="An empty item is erroneously saved."
        ) as cm:
            item = models.Item(content="", list=todo_list)
            item.full_clean()
            item.save()
        self.assertIn(
            "This field cannot be blank.",
            cm.exception.message_dict['content']
        )

    def test_can_not_add_same_item_to_a_list(self):
        todo_list = models.List.objects.create()
        text = "something"
        item1 = models.Item(content=text, list=todo_list)
        item1.save()
        item2 = models.Item(content=text, list=todo_list)
        with self.assertRaises(
                ValidationError,
                msg="Duplicated items shouldn't be added to a list."
        ) as cm:
            item2.full_clean()

    def test_can_add_same_item_to_different_list(self):
        text = "sef"
        list1 = models.List.objects.create()
        list2 = models.List.objects.create()
        item1 = models.Item(content=text, list=list1)
        item2 = models.Item(content=text, list=list2)
        item1.full_clean() # should not raise
        item2.full_clean() # should not raise


class ListModelTest(TestCase):

    def test_list_url(self):
        todo_list = models.List.objects.create()
        self.assertEqual(
            todo_list.get_absolute_url(),
            f"/lists/{todo_list.pk}/"
        )

    def test_list_can_belongs_to_no_one(self):
        list = models.List.objects.create()
        self.assertIsNone(list.user)

    def test_list_can_belongs_to_an_user(self):
        user = get_user_model().objects.create_user(email="test@gmail.com")
        list = models.List.objects.create(user=user)
        self.assertEqual(list.user, user)

    def test_list_name_is_empty_string_if_no_entry(self):
        list = models.List.objects.create()
        self.assertEqual(list.name, "")

    def test_list_name_equals_to_first_item_content(self):
        list = models.List.objects.create()
        models.Item.objects.create(content="sef", list=list)
        self.assertEqual(list.name, "sef")

    def test_can_create_new_list_with_first_item(self):
        content = "sef"
        list = models.List.objects.create_new(first_item=content)
        self.assertEqual(list.entries.get().content, content)

    def test_can_create_new_list_with_user(self):
        content = "sef"
        user = get_user_model().objects.create_user(email="test@gmail.com")
        list = models.List.objects.create_new(
            first_item=content, user=user
        )
        self.assertEqual(user.lists.get(), list)

    def test_can_create_new_list_without_user(self):
        content = "sef"
        list = models.List.objects.create_new(
            first_item=content, user=None,
        )
        self.assertIsNone(list.user)

from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError

from .. import models


class ListAndItemModelTest(TestCase):

    def test_saving_and_get_items(self):
        todo_list = models.List.objects.create()
        item1_text = "new item1"
        item2_text = "new item2"
        item1 = models.Item(
            content=item1_text,
            create_time=timezone.now(),
            list=todo_list,
        )
        item1.save()
        item2 = models.Item(
            content=item2_text,
            create_time=timezone.now(),
            list=todo_list
        )
        item2.save()
        self.assertEqual(models.Item.objects.count(), 2)
        self.assertEqual(
            models.Item.objects.get(content=item1_text).content,
            item1.content
        )
        self.assertEqual(
            models.Item.objects.get(content=item2_text).content,
            item2.content
        )
        self.assertEqual(todo_list.entries.count(), 2)


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

    def test_list_url(self):
        todo_list = models.List.objects.create()
        self.assertEqual(
            todo_list.get_absolute_url(),
            f"/lists/{todo_list.pk}/"
        )

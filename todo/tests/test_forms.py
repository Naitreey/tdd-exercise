from django.test import TestCase
from django.core.exceptions import ValidationError

from .. import forms, models

class ItemFormTest(TestCase):

    def test_can_save_item(self):
        content = "somtehing"
        list = models.List.objects.create()
        form = forms.ItemForm(data={"content": content})
        form.save(list=list)
        self.assertEqual(list.entries.count(), 1)
        self.assertEqual(list.entries.first().content, content)

    def test_can_not_save_empty_item(self):
        content = ""
        list = models.List.objects.create()
        form = forms.ItemForm(data={"content": content})
        with self.assertRaisesRegex(
                ValueError, r"the data didn't validate",
                msg="An empty item is erroneously saved."
        ) as cm:
            form.save(list=list)

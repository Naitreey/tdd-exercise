from django import forms
from django.core.exceptions import ValidationError

from . import models


EMPTY_CONTENT_ERROR = "To-Do entry can not be empty."


class NewListItemForm(forms.ModelForm):

    class Meta:
        model = models.Item
        fields = ["content"]
        error_messages = {
            "content": {
                "required": EMPTY_CONTENT_ERROR,
            }
        }

    def save(self, list):
        instance = super().save(commit=False)
        instance.list = list
        instance.save()
        self.save_m2m()


class ExistingListItemForm(forms.ModelForm):

    class Meta:
        model = models.Item
        fields = ["content"]
        error_messages = {
            "content": {
                "required": EMPTY_CONTENT_ERROR,
            }
        }

    def __init__(self, list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.todolist = list
        self.duplicate = None

    def clean_content(self):
        message = f'"%(content)s" already exists, please enter something else.'
        content = self.cleaned_data['content']
        try:
            dup = self.todolist.entries.get(content=content)
        except models.Item.DoesNotExist:
            return content
        else:
            # mark duplicate item for external inspection
            self.duplicate = dup
            raise ValidationError(
                message=message, 
                code="duplicate", 
                params={"content": content}
            )

    def save(self):
        instance = super().save(commit=False)
        instance.list = self.todolist
        instance.save()
        self.save_m2m()

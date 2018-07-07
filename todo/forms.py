from django.forms import ModelForm

from . import models


class NewListItemForm(ModelForm):

    def save(self, list):
        instance = super().save(commit=False)
        instance.list = list
        instance.save()
        self.save_m2m()

    class Meta:
        model = models.Item
        fields = ["content"]
        error_messages = {
            "content": {
                "required": "To-Do entry can not be empty.",
            }
        }

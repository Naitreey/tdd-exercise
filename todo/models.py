from django.db import models
from django.urls import reverse


class List(models.Model):

    create_time = models.DateTimeField(
        verbose_name="Create time",
        auto_now_add=True,
        null=False,
        blank=False,
        help_text="When it's created",
    )

    class Meta:
        verbose_name = "To-Do List"
        verbose_name_plural = f"{verbose_name}s"

    def __str__(self):
        return f"{self.create_time}"

    def get_absolute_url(self):
        return reverse("view-list", kwargs={"pk": self.pk})


class Item(models.Model):

    content = models.CharField(
        verbose_name="Content",
        max_length=1024,
        db_index=True,
        help_text="todo entry text",
        blank=False,
        null=False,
    )
    create_time = models.DateTimeField(
        verbose_name="Create time",
        auto_now_add=True,
        null=False,
        blank=False,
        help_text="When it's created",
    )
    list = models.ForeignKey(
        List,
        verbose_name="List",
        blank=False,
        null=False,
        related_name="entries",
        help_text="The list where the item belongs to",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "List item"
        verbose_name_plural = f"{verbose_name}s"
        unique_together = ("content", "list")

    def __str__(self):
        return f"{self.list} | {self.content} | {self.create_time}"

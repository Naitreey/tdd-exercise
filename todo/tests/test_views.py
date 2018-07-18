from datetime import timedelta
from unittest import skip
import html

from django.test import TestCase
from django.urls import resolve
from django.http.request import HttpRequest
from django.template import loader
from django.utils import timezone

from .. import views, models, forms


class HomePageTest(TestCase):

    def test_resolve(self):
        homepage_view = resolve("/").func
        self.assertEqual(homepage_view, views.home)

    def test_can_get_homepage(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "todo/index.html")
        self.assertEqual(response.status_code, 200)

    def test_homepage_has_form(self):
        response = self.client.get("/")
        self.assertIsInstance(response.context['form'], forms.NewListItemForm)

    def test_get_not_save_item(self):
        self.client.get("/")
        self.assertEqual(models.Item.objects.count(), 0)


class ListViewTest(TestCase):

    def setUp(self):
        self.todolist = models.List.objects.create()

    def test_list_template_used(self):
        todo_list = self.todolist
        response = self.client.get(f"/lists/{todo_list.pk}/")
        self.assertTemplateUsed(response, "todo/list.html")
        self.assertEqual(response.status_code, 200)

    def test_list_page_context(self):
        todo_list = self.todolist
        response = self.client.get(f"/lists/{todo_list.pk}/")
        self.assertIn("items", response.context)
        self.assertIsInstance(response.context['form'], forms.ExistingListItemForm)
        self.assertIsInstance(response.context['list'], models.List)

    def test_list_only_display_belonging_items(self):
        todo_list = self.todolist
        todo_list2 = models.List.objects.create()
        models.Item.objects.bulk_create([
            models.Item(
                content="item 1", 
                list=todo_list, 
                create_time=timezone.now()
            ),
            models.Item(
                content="item 2", 
                list=todo_list, 
                create_time=timezone.now()+timedelta(seconds=1)
            ),
        ])
        models.Item.objects.bulk_create([
            models.Item(content="item 3", list=todo_list2),
            models.Item(content="item 4", list=todo_list2),
        ])
        response = self.client.get(f"/lists/{todo_list.pk}/")
        self.assertContains(response, "item 1")
        self.assertContains(response, "item 2")
        self.assertNotContains(response, "item 3")
        self.assertNotContains(response, "item 4")

    def test_can_add_item_to_list(self):
        todo_list = self.todolist
        list_url = todo_list.get_absolute_url()
        text = "something"
        response = self.client.post(list_url, data={"content": "something"})
        self.assertRedirects(response, list_url)
        self.assertEqual(todo_list.entries.count(), 1)
        response = self.client.get(list_url)
        self.assertContains(response, text)

    def test_can_not_post_same_item_to_list(self):
        text = "something"
        response = self.post_same_item(text)
        self.assertTemplateUsed(response, "todo/list.html")
        self.assertContains(
            response,
            html.escape(
                f'"{text}" already exists, please enter something else.'
            ),
        )
        self.assertEqual(self.todolist.entries.count(), 1)

    def test_highlight_dup_item_when_same_item_is_posted(self):
        response = self.post_same_item("something")
        self.assertContains(response, "duplicate")

    def post_same_item(self, text):
        todo_list = self.todolist
        list_url = todo_list.get_absolute_url()
        response = self.client.post(list_url, data={"content": text})
        response = self.client.post(list_url, data={"content": text})
        return response


class InitialListTest(TestCase):

    def test_has_initial_list(self):
        self.assertEqual(models.List.objects.count(), 1)


class NewListTest(TestCase):

    new_list_url = "/lists/"

    def test_can_post_new_item(self):
        response = self.client.post(
            self.new_list_url,
            data={"content": "new item"}
        )
        list = models.List.objects.last()
        self.assertRedirects(response, f"/lists/{list.pk}/")

    def test_new_lists_have_different_urls(self):
        response1 = self.client.post(
            self.new_list_url,
            data={"content": "new item"}
        )
        response2 = self.client.post(
            self.new_list_url,
            data={"content": "new item"}
        )
        self.assertNotEqual(response1['Location'], response2['Location'])

    def test_can_save_new_item(self):
        text = "new item"
        response = self.client.post(
            self.new_list_url,
            data={"content": text}
        )
        self.assertEqual(models.Item.objects.count(), 1)
        self.assertEqual(models.Item.objects.first().content, text)

    def test_can_not_post_empty_item(self):
        response = self.client.post(
            self.new_list_url,
            data={"content": ""}
        )
        self.assertEqual(models.Item.objects.count(), 0)

    def test_post_empty_item_returns_homepage(self):
        response = self.client.post(
            self.new_list_url,
            data={"content": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo/index.html")
        self.assertIsInstance(response.context['form'], forms.NewListItemForm)

    def test_post_empty_item_shows_invalidation(self):
        response = self.client.post(
            self.new_list_url,
            data={"content": ""}
        )
        self.assertContains(response, "To-Do entry can not be empty.")

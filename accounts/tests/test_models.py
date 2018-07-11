from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.exceptions import ValidationError

from .. import models


class UserModelTest(TestCase):

    test_email = "test@test.test"

    def test_user_model_is_correct(self):
        self.assertIs(models.User, get_user_model())

    def test_can_create_normal_user(self):
        user = models.User.objects.create_user(email=self.test_email)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_can_create_superuser(self):
        su = models.User.objects.create_superuser(email=self.test_email)
        self.assertTrue(su.is_staff)
        self.assertTrue(su.is_superuser)

    def test_can_get_user_by_uidb64(self):
        user = models.User.objects.create_user(email=self.test_email)
        user2 = models.User.objects.get_by_uidb64(
            urlsafe_base64_encode(force_bytes(user.pk))
        )
        self.assertEqual(user, user2)

    def test_can_not_has_empty_email(self):
        email = ""
        user = models.User(email=email)
        with self.assertRaises(ValidationError) as cm:
            user.full_clean()

    def test_can_not_has_invalid_email(self):
        email = "sef"
        user = models.User(email=email)
        with self.assertRaises(ValidationError) as cm:
            user.full_clean()

    def test_only_email_is_needed(self):
        user = models.User(email=self.test_email)
        user.full_clean() # should not raise ValidationError
        user.save()

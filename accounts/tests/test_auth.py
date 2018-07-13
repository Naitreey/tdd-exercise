from django.test import TestCase
from django.contrib.auth import authenticate

from .. import models
from ..auth.backends import TokenBackend


class TokenBackendTest(TestCase):

    registered_email = "test@gmail.com"

    def setUp(self):
        self.user = models.User.objects.create_user(
            email=self.registered_email
        )

    def test_can_get_registered_user(self):
        backend = TokenBackend()
        self.assertEqual(backend.get_user(self.user.pk), self.user)

    def test_can_not_get_unknown_user(self):
        backend = TokenBackend()
        self.assertIsNone(backend.get_user(1223))

    def test_can_authenticate_registered_user(self):
        backend = TokenBackend()
        self.assertEqual(
            backend.authenticate(
                None,
                uidb64=self.user.uidb64,
                token=self.user.make_auth_token(),
            ),
            self.user,
        )

    def test_can_not_authenticate_unknown_user(self):
        backend = TokenBackend()
        self.assertIsNone(
            backend.authenticate(
                None,
                uidb64="",
                token="",
            )
        )


class AuthTest(TestCase):

    registered_email = "test@gmail.com"

    def setUp(self):
        self.user = models.User.objects.create_user(
            email=self.registered_email
        )

    def test_can_authenticate_registered_user(self):
        user = authenticate(
            uidb64=self.user.uidb64,
            token=self.user.make_auth_token(),
        )
        self.assertEqual(user, self.user)

    def test_can_not_authenticate_dummy_credentials(self):
        user = authenticate(uidb64="", token="")
        self.assertIsNone(user)

    def test_can_not_authenticate_without_credentials(self):
        user = authenticate()
        self.assertIsNone(user)

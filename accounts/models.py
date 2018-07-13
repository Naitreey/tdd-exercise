from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes


class UserManager(BaseUserManager):

    def get_by_uidb64(self, uidb64):
        # urlsafe_base64_decode() decodes to bytestring
        uid = urlsafe_base64_decode(uidb64).decode()
        return self.get(pk=uid)

    def create_user(self, email, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email=email, **extra_fields)

    def create_superuser(self, email, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email=email, **extra_fields)

    def _create_user(self, email, **extra_fields):
        instance = self.model(email=email, **extra_fields)
        instance.save(using=self.db)
        return instance


class User(PermissionsMixin, AbstractBaseUser):

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    email = models.EmailField(
        verbose_name="Email",
        null=False,
        blank=False,
        unique=True,
        help_text="User's email address",
    )
    password = ""

    class Meta:
        verbose_name = "User account"
        verbose_name_plural = "User accounts"

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def uidb64(self):
        return urlsafe_base64_encode(force_bytes(self.pk))

    def make_auth_token(self):
        return default_token_generator.make_token(self)

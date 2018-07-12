from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.http import urlsafe_base64_decode


class UserManager(BaseUserManager):

    def get_by_uidb64(self, uidb64):
        uid = urlsafe_base64_decode(uidb64)
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

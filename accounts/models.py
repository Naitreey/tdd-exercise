from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.http import urlsafe_base64_decode


class UserManager(BaseUserManager):

    def _create_user(self, email, **extra_fields):
        email = self.normalize_email(email)
        instance = self.model(email=email, **extra_fields)
        instance.save(using=self.db)
        return instance

    def create_user(self, email, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, **extra_fields)

    def create_superuser(self, email, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, **extra_fields)

    def get_by_uidb64(self, uidb64):
        uid = urlsafe_base64_decode(uidb64)
        return self.get(pk=uid)


class User(PermissionsMixin, AbstractBaseUser):

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    email = models.CharField(max_length=255, unique=True)

    @property
    def is_staff(self):
        return True

    @property
    def is_active(self):
        return True

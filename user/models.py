from typing import Type
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):
        if not password:
            raise ValueError('User must have a password.')
        if not email:
            raise ValueError("User must have an email.")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        if not password:
            raise ValueError('Admins must have a password.')
        if not email:
            raise ValueError('Admins must have an email.')

        user = self.create_user(email, password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractUser):

    email = models.EmailField(
        blank=False, max_length=255, verbose_name="email", unique=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    uuid = models.CharField(max_length=10)

    def __str__(self):
        return self.uuid


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# -*- coding: utf-8 -*-
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from project.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_staff and self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_staff and self.is_superuser

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

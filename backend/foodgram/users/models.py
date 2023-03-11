from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


from .validators import validate_username


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, last_login=None, **kwargs):
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(email=email,
                          is_staff=True,
                          is_superuser=True,
                          **kwargs)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    username = models.CharField(
        validators=(validate_username,),
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )

    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )

    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True,
    )

    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )

    password = models.CharField(
        'Пароль',
        max_length=150,
        null=False,
    )

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('id',)


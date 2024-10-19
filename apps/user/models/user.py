from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractUser,
    UserManager as BaseUserManager,
)
from django.db import models

from apps.common.models import BaseModel
from apps.portfolio.models import Portfolio


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Overridden from base manager to create a user without username.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        """
        Overridden from base manager to create a user without username.
        """
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        """
        Overridden from base manager to create a superuser without username.
        """
        extra_fields.update({
            "is_active": True,
            "is_staff": True,
            "is_superuser": True,
        })
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, BaseModel):
    email = models.EmailField(
        verbose_name=_("email address"),
        unique=True,
    )
    username = None

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def portfolio_count(self):
        return self.portfolios.count()

    @property
    def portfolio(self) -> Portfolio | None:
        return self.portfolios.first()

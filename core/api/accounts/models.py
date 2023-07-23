from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxLengthValidator, EmailValidator

from core.general.validators import HexStringValidator
from core.general.constants import ACCOUNT_ID_LENGTH, USER_NAME_LENGTH
from core.api.creators.models import Creator
from core.api.businesses.models import Business
from .managers import AccountManager


class Account(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = 'accounts'
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    class Roles(models.TextChoices):
        CREATOR = 'CREATOR', 'creator'
        BUSINESS = 'BUSINESS', 'business'

    # Created at account creation
    id = models.TextField(
        primary_key=True,
        unique=True,
        validators=[
            HexStringValidator(ACCOUNT_ID_LENGTH),
            MaxLengthValidator(ACCOUNT_ID_LENGTH),
        ]
    )
    username = models.TextField(
            unique=True,
            validators=[MaxLengthValidator(USER_NAME_LENGTH)]
        )
    password = models.TextField()
    email = models.EmailField(
            unique=True,
            validators=[EmailValidator()]
        )
    role = models.TextField(choices=Roles.choices)
    balance = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Input at account edit
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)

    objects = AccountManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def has_module_perms(self, app_label):
        return self.is_superuser

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def save(self, *args, **kwargs):
        is_new_account = self._state.adding
        super().save(*args, **kwargs)
        if is_new_account:
            if self.role == Account.Roles.CREATOR:
                Creator.objects.create(account_id=self)
            elif self.role == Account.Roles.BUSINESS:
                Business.objects.create(account_id=self)

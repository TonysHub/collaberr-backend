from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings

from core.general.validators import HexStringValidator
from core.general.constants import ACCOUNT_ID_LENGTH, USER_NAME_LENGTH
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
    id = models.CharField(
            max_length=ACCOUNT_ID_LENGTH,
            primary_key=True,
            unique=True,
            validators=[HexStringValidator(ACCOUNT_ID_LENGTH)],
            )
    username = models.CharField(max_length=USER_NAME_LENGTH, unique=True)
    password = models.CharField(max_length=25)
    email = models.EmailField(max_length=50, unique=True)
    role = models.CharField(max_length=50, choices=Roles.choices)
    balance = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Updated at account edit
    first_name = models.CharField(max_length=25, blank=True)
    last_name = models.CharField(max_length=25, blank=True)
    
    objects = AccountManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return f'{self.username}'
    
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

class Creator(models.Model):
    class Meta:
        db_table = 'creators'
        verbose_name = 'Creator'
        verbose_name_plural = 'Creators'
    
    account_id = models.OneToOneField(
            settings.AUTH_USER_MODEL, 
            on_delete=models.CASCADE,
            primary_key=True,
            related_name='creator',
            db_column='account_id',
            )
    earnings = models.PositiveIntegerField(default=0)

class Business(models.Model):
    class Meta:
        db_table = 'businesses'
        verbose_name = 'Business'
        verbose_name_plural = 'Businesses'

    account_id = models.OneToOneField(
            settings.AUTH_USER_MODEL, 
            on_delete=models.CASCADE,
            primary_key=True,
            related_name='business',
            db_column='account_id',
            )










    
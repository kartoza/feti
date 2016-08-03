"""
Adapted from http://stackoverflow.com/a/12648124/1158060
"""


from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff_user(self, username, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        u = self.create_user(
            username,
            password=password,
            date_of_birth=date_of_birth
        )
        u.is_admin = True
        u.save(using=self._db)
        return u


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    user_name = models.CharField(
        help_text="Please choose a unique user name.",
        max_length=20,
        unique=True
    )
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: "
                "'+6288888888888'. Up to 15 digits allowed.")
    phone = models.CharField(
        validators=[phone_regex], blank=True, max_length=15
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email', 'phone']

    def __unicode__(self):
        return self.email

    def has_permission(self, permission, obj=None):
        "Does the user have a specific permission?"
        if self.is_staf:
            return True
        return False

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        if self.is_staf:
            return True
        return False

    @property
    def is_staff(self):
        "Is the user a member of staff."
        return self.is_admin and self.is_active

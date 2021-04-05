"""Module with data models of account app."""
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Custom user manager."""

    def _create_user(self, phone, password, **extra_fields):
        """Create and save a user with the given phone and password."""
        if not phone:
            raise ValueError(_('Users must have an phone number.'))

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_user(self, phone=None, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model class."""
    avatar = models.ImageField(_('Avatar'), upload_to='avatar', null=True, blank=True)
    display_name = models.CharField(_('Display name'), max_length=40, blank=True)
    phone = models.CharField(_('Telephone'), max_length=20, unique=True)
    email = models.EmailField(_('Email'), unique=True, blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    is_admin = models.BooleanField(_('Admin'), default=False)
    is_verified = models.BooleanField(_('Verified'), default=False)
    is_advertiser = models.BooleanField(_('Advertiser'), default=False)
    is_company = models.BooleanField(_('Company'), default=False)
    is_plus = models.BooleanField(_('Plus'), default=False)
    date_joined = models.DateTimeField(_('Date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    EMAIL_FIELD = 'email'

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def get_display_name(self):
        """Returns the display name."""
        return self.display_name or self.get_phone_number_display()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Sends an email to this User."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
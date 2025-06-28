from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from datetime import timedelta
class UserManager(BaseUserManager):
    """
    Custom manager for User model.
    """
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser):
    """
    Custom User model that uses email as the unique identifier.
    """
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = '01. Users'
        ordering = ['id']

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return self.is_admin

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return self.is_admin


class OTP(models.Model):
    """
    Model to store One-Time Passwords (OTPs) for users.
    """
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    otp_hashed = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'OTP'
        verbose_name_plural = '03. OTPs'

    def __str__(self):
        return f'{self.user.email} - OTP created at {self.created_at}'

    def set_otp(self, raw_otp):
        self.otp_hashed = make_password(raw_otp)

    def verify_otp(self, raw_otp):
        if not self.is_valid():
            return False
        return check_password(raw_otp, self.otp_hashed)

    def is_valid(self):
        return timezone.now() <= self.created_at + timedelta(minutes=15)


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin

# Create your models here.


class CustomUserManager(UserManager):
    def _create_user(self, username, password, email, **extra_fields):
        if not email:
            raise ValueError("You have not provided a vaild email address")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, password=None, username=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(
        self, username=None, email=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(username, password, email, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # DEFAULT FIELD
    email = models.EmailField(("email address"), unique=True)
    password = models.CharField(max_length=200)
    username = models.CharField(max_length=200, null=False, blank=False, unique=True)

    firstName = models.CharField(max_length=300, null=True, blank=True)
    lastName = models.CharField(max_length=300, null=True, blank=True)
    phone = models.CharField(max_length=300, null=True, blank=True)
    dateOfBirth = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username
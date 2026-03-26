from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Phone number is required")

        user = self.model(
            phone=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    caste = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    
    # Cooldown: user cannot request items until this date passes
    cooldown_until = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone

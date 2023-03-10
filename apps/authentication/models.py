from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.utils import timezone
from role_permission.models import Roles


class User(AbstractUser):
    username = None
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, default=None, null=True,
                             db_constraint=False, related_name='role_user')
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # Custom Object manager
    objects = CustomUserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name

    class Meta:
        db_table = "users"

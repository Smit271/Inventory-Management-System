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
    gender = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL, related_name='%(class)s_created_by', null=True, blank=True)
    updated_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL, related_name='%(class)s_updated_by', null=True, blank=True)

    # CUSTOM OBJECT MANAGER
    objects = CustomUserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name

    def get_user_details(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'date_joined': self.date_joined,
        }

    # CAN CUSTOMIZE IN-BUILT METHOD FOR MORE VALIDATIONS
    # def save(self):
    #     print("===> SAVING METHOD IS CALLED")
    #     return super().save()

    class Meta:
        db_table = "users"


# class Employee(models.Model):
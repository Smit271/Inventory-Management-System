from django.contrib.auth.models import BaseUserManager, UserManager
from role_permission.models import Roles


class CustomUserManager(UserManager):
    def get_queryset(self):
        return super(CustomUserManager, self).get_queryset().filter(
            # is_active=True,
            is_delete=False
        ).select_related('created_by', 'updated_by')

    def create_user(self, email, password=None):
        if not email:
            msg = 'User must have an email address'
            raise ValueError(msg)

        user = self.model(email=UserManager.normalize_email(email))

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return

    def create_employee(self, email, password=None):
        if not email:
            msg = 'User must have an email address'
            raise ValueError(msg)

        user = self.model(email=UserManager.normalize_email(email))

        user.set_password(password)
        emp_role, _ = Roles.objects.get_or_create(name="Employee")
        user.role = emp_role
        user.save()
        return user

from django.contrib.auth.models import BaseUserManager, UserManager


class CustomUserManager(UserManager):
    def get_queryset(self):
        return super(CustomUserManager, self).get_queryset().filter(
            is_active=True,
            is_delete=False
        )

    def create_user(self, email, password=None):
        if not email:
            msg = 'Users must have an email address'
            raise ValueError(msg)

        user = self.model(email=UserManager.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

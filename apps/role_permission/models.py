from django.db import models


class Permissions(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)
    is_delte = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}- {self.code}"

    class Meta:
        db_table = 'permissions'


class Roles(models.Model):
    name = models.CharField(max_length=255)
    permissions = models.ManyToManyField(
        Permissions, related_name='roles_permission')
    created_by = models.ForeignKey(
        'authentication.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_delte = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'roles'

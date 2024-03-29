from django.db import models
from .managers import PermissionManager, RolesManager


class Permissions(models.Model):
    table_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL, related_name='%(class)s_created_by', null=True, blank=True)
    updated_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL, related_name='%(class)s_updated_by', null=True, blank=True)

    objects = PermissionManager()

    def __str__(self):
        return f"{self.name}- {self.code}"

    class Meta:
        db_table = 'permissions'


class Roles(models.Model):
    name = models.CharField(max_length=255)
    permissions = models.ManyToManyField(
        Permissions, related_name='roles_permission')
    created_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL, related_name='%(class)s_created_by', null=True, blank=True)
    updated_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL, related_name='%(class)s_updated_by', null=True, blank=True)

    objects = RolesManager()

    def __str__(self):
        return self.name

    def get_full_details(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_by_id': self.created_by.id if self.created_by else None,
            'created_by_name': self.created_by.name if self.created_by else None,
            'permissions': list(self.permissions.values()),
            'permissions_list': [id['id'] for id in self.permissions.values('id')],
        }

    class Meta:
        db_table = 'roles'

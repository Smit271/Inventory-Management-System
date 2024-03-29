from django.db import models


class PermissionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            is_active=True,
            is_delete=False
        ).select_related('created_by', 'updated_by')


class RolesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            is_active=True,
            is_delete=False
        ).select_related('created_by', 'updated_by')

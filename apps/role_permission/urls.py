from django.urls import path
from .views import (
    permission, get_permission_detail, add_permission_data, edit_permission_data,
    delete_permission,
    role, add_role, create_role,
    get_role_detail, edit_role_data
)

urlpatterns = [
    # ---------- PERMISSIONS URLS ----------
    path('permission', permission, name='permissions'),
    path('get_permission_detail/<int:id>',
         get_permission_detail, name='get_permission_detail'),
    path('add_permission_data', add_permission_data, name='add_permission_data'),
    path('edit_permission_data', edit_permission_data,
         name='edit_permission_data'),
    path('delete_permission', delete_permission, name='delete_permission'),

    # ---------- ROLES URLS ----------
    path('role', role, name='role'),
    path('add_role', add_role, name='add_role'),
    path('create_role', create_role, name='create_role'),
    path('get_role_detail/<int:id>',
         get_role_detail, name='get_role_detail'),
    path('edit_role_data', edit_role_data,
         name='edit_role_data'),
    # path('delete_role', delete_role, name='delete_role'),
]

from django.urls import path
from .views import (
    permissions, get_permissions_detail, add_permissions_data, edit_permissions_data,
    delete_permissions
)

urlpatterns = [
    # Products URLs
    path('permissions', permissions, name='permissions'),
    path('get_permissions_detail/<int:id>',
         get_permissions_detail, name='get_permissions_detail'),
    path('add_permissions_data', add_permissions_data, name='add_permissions_data'),
    path('edit_permissions_data', edit_permissions_data, name='edit_permissions_data'),
    path('delete_permissions', delete_permissions, name='delete_permissions'),
]

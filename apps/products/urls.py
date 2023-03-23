from django.urls import path
from .views import (
    home, get_product_detail, add_product_data, edit_product_data,
    delete_product,
    device_type, get_device_type_detail, add_device_type_data, edit_device_type_data,
    delete_device_type,
    location, get_location_detail, add_location_data, edit_location_data,
    delete_location
)

urlpatterns = [
    # ----- Products URLs ----- #
    path('home', home, name='home'),
    path('get_product_detail/<int:id>',
         get_product_detail, name='get_product_detail'),
    path('add_product_data', add_product_data, name='add_product_data'),
    path('edit_product_data', edit_product_data, name='edit_product_data'),
    path('delete_product', delete_product, name='delete_product'),

    # ----- Device Type URLs ----- #
    path('device_type', device_type, name='device_type'),
    path('get_device_type_detail/<int:id>',
         get_device_type_detail, name='get_device_type_detail'),
    path('add_device_type_data', add_device_type_data,
         name='add_device_type_data'),
    path('edit_device_type_data', edit_device_type_data,
         name='edit_device_type_data'),
    path('delete_device_type', delete_device_type, name='delete_device_type'),

    # ----- Location Type URLs ----- #
    path('location', location, name='location'),
    path('get_location_detail/<int:id>',
         get_location_detail, name='get_location_detail'),
    path('add_location_data', add_location_data, name='add_location_data'),
    path('edit_location_data', edit_location_data, name='edit_location_data'),
    path('delete_location', delete_location, name='delete_location'),
]

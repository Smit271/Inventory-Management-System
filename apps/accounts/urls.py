from django.urls import path
from .views import (
    dashboard,
    login_view, add_user,
    create_user, users, delete_user,
    get_user_detail, edit_user_data,
    employees, add_employee, create_employee,
    get_employee_detail, delete_employee,
    edit_employee_data
)

urlpatterns = [
    path('sign_in', login_view, name='login_view'),
    path('dashboard', dashboard, name='dashboard'),

    # ----- URLS FOR USER ----- #
    path('users', users, name='users'),
    path('add_user', add_user, name='add_user'),
    path('create_user', create_user, name='create_user'),
    path('get_user_detail/<int:id>', get_user_detail, name='get_user_detail'),
    path('delete_user', delete_user, name='delete_user'),
    path('edit_user_data', edit_user_data, name='edit_user_data'),

    # ----- URLS FOR EMPLOYEES ----- #
    path('employees', employees, name='employees'),
    path('add_employee', add_employee, name='add_employee'),
    path('create_employee', create_employee, name='create_employee'),
    path('get_employee_detail/<int:id>', get_employee_detail, name='get_employee_detail'),
    path('delete_employee', delete_employee, name='delete_employee'),
    path('edit_employee_data', edit_employee_data, name='edit_employee_data'),
]
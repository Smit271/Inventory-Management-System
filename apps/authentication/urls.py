from django.urls import path
from .views import (
    dashboard,
    login_view, add_user,
    create_user, users
)

urlpatterns = [
    path('sign_in', login_view, name='login_view'),
    path('dashboard', dashboard, name='dashboard'),

    # ----- URLS FOR USER ----- #
    path('users', users, name='users'),
    path('add_user', add_user, name='add_user'),
    path('create_user', create_user, name='create_user'),
]
from django.urls import path
from .views import (
    login_view
)

urlpatterns = [
    path('sign_in', login_view, name='login_view'),
]
from django.urls import path
from .views import admin_login

urlpatterns = [
    # ... autres URLs ...
    path('admin/login/', admin_login, name='admin_login'),
]

from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User


admin.site.register(User)
admin.site.site_header = 'Управление авторизацией'

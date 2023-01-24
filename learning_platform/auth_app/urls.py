from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('change-password/', views.change_password),
    path('reset-password/', views.reset_password),
]
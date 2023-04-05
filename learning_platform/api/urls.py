from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.courses, name='courses'),
    path('courses/<int:course_id>', views.courses_id, name='courses_id'),
    path('analytics/', views.analytics, name='analytics'),
    path('users/', views.users, name='users'),
]

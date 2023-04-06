from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.CourseAPIView.as_view(), name='courses'),
    path('courses/<int:course_id>', views.courses_id, name='courses_id'),
    path('analytics/', views.analytics, name='analytics'),
    path('users/', views.users, name='users'),
]

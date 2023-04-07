from django.urls import path
from .views import *

urlpatterns = [
    path('courses/', CourseListAPIView.as_view(), name='courses'),
    path('courses/<int:course_id>', CourseRetrieveAPIView.as_view(), name='courses_id'),
    path('analytics/', analytics, name='analytics'),
    path('users/', users, name='users'),
]

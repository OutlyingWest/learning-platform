from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.CourseListAPIView.as_view(), name='courses'),
    path('courses/<int:id>', views.CourseRetrieveAPIView.as_view(), name='courses_id'),
    path('analytics/', views.analytics, name='analytics'),
    path('users/', views.users, name='users'),
]

from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

urlpatterns = [
    path('courses/', CourseListAPIView.as_view(), name='courses'),
    path('courses/<int:course_id>/', CourseRetrieveAPIView.as_view(), name='courses_id'),
    path('analytics/', analytics, name='analytics'),
    path('users/', users, name='users'),
    # Authentication urls
    path('authentication/', include('rest_framework.urls')),
    path('generate-token/', obtain_auth_token, name='generate-token'),
    path('users-for-admin/', UserForAdminView.as_view(), name='users-for-admin'),
    path('courses/create/', CourseCreateView.as_view(), name='courses_create'),
    path('courses/delete/<int:course_id>/', CourseDeleteView.as_view(), name='courses_delete'),
]


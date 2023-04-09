from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter(trailing_slash=True)
router.register('analytics', AnalyticViewSet, basename='analytic')
router.register('trackings', TrackingStudentViewSet, basename='tracking')
router.register('trackings_for_authors', TrackingAuthorViewSet, basename='tracking_for_authors')

for url in router.urls:
    print(url)

urlpatterns = [
    path('courses/', CourseListAPIView.as_view(), name='courses'),
    path('courses/<int:course_id>/', CourseRetrieveAPIView.as_view(), name='courses_id'),
    path('users/', users, name='users'),
    path('', include(router.urls)),

    # Authentication urls
    path('authentication/', include('rest_framework.urls')),
    path('generate-token/', obtain_auth_token, name='generate-token'),
    path('users-for-admin/', UserForAdminView.as_view(), name='users-for-admin'),
    path('courses/create/', CourseCreateView.as_view(), name='courses_create'),
    path('courses/delete/<int:course_id>/', CourseDeleteView.as_view(), name='courses_delete'),
]


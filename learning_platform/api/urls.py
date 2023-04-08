from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

urlpatterns = [
    path('courses/', CourseListAPIView.as_view(), name='courses'),
    path('courses/<int:course_id>/', CourseRetrieveAPIView.as_view(), name='courses_id'),
    path('users/', users, name='users'),

    path('analytics/', AnalyticViewSet.as_view(actions={'get': 'list'}), name='analytics'),
    path('analytics/<int:course_id>', AnalyticViewSet.as_view(actions={'get': 'retrieve'}), name='analytics_id'),

    path('trackings/', TrackingStudentViewSet.as_view(actions={'get': 'list', 'post': 'create'}), name='trackings'),
    path('trackings/<int:course_id>', TrackingStudentViewSet.as_view(actions={'get': 'retrieve'}), name='trackings_id'),

    path('trackings_for_authors/', TrackingAuthorViewSet.as_view(
        actions={
            'get': 'list', 'post': 'create', 'patch': 'partial_update'
        }),
        name='trackings_for_authors'),
    path('trackings_for_authors/<int:course_id>', TrackingAuthorViewSet.as_view(actions={'get': 'retrieve'}),
         name='trackings_for_authors_id'),
    # Authentication urls
    path('authentication/', include('rest_framework.urls')),
    path('generate-token/', obtain_auth_token, name='generate-token'),
    path('users-for-admin/', UserForAdminView.as_view(), name='users-for-admin'),
    path('courses/create/', CourseCreateView.as_view(), name='courses_create'),
    path('courses/delete/<int:course_id>/', CourseDeleteView.as_view(), name='courses_delete'),
]


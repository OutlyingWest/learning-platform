from django.views.decorators.cache import cache_control, never_cache
from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('create/', CourseCreateView.as_view(), name='create'),
    path('delete/<int:course_id>/', CourseDeleteView.as_view(), name='delete'),
    path('update/<int:course_id>/', CourseUpdateView.as_view(), name='update'),
    re_path('^detail/(?P<course_id>[1-9]+[0-9]*)/$', cache_control(max_age=600)(CourseDetailView.as_view()),
            name='detail'),
    path('enroll/<int:course_id>/', enroll, name='enroll'),
    path('review/<int:course_id>/', review, name='review'),
    path('<int:course_id>/create_lesson/', LessonCreateView.as_view(), name='create_lesson'),
    # Session work paths
    path('add_favorite/<int:course_id>/', add_course_to_favorites, name='add_favorite'),
    path('remove_favorite/<int:course_id>/', remove_course_from_favorites, name='remove_favorite'),
    path('favorites/', never_cache(FavoriteCoursesView.as_view()), name='favorites'),
    path('settings/', SettingsFormView.as_view(), name='settings'),
    path('get_certificate/<int:course_id>/', get_certificate_view, name='get_certificate'),
    path('tracking/', TrackingView.as_view(), name='tracking'),
    #API urls
    path('api_courses/', api_courses, name='api_courses'),
]

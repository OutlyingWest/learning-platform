from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.MainView.as_view(), name='index'),
    path('create/', views.CourseCreateView.as_view(), name='create'),
    path('delete/<int:course_id>/', views.CourseDeleteView.as_view(), name='delete'),
    path('update/<int:course_id>/', views.CourseUpdateView.as_view(), name='update'),
    re_path('^detail/(?P<course_id>[1-9]+[0-9]*)/$', views.CourseDetailView.as_view(), name='detail'),
    path('enroll/<int:course_id>/', views.enroll, name='enroll'),
    path('review/<int:course_id>/', views.review, name='review'),
    path('<int:course_id>/create_lesson/', views.LessonCreateView.as_view(), name='create_lesson'),
    # Session work paths
    path('add_favorite/<int:course_id>/', views.add_course_to_favorites, name='add_favorite'),
    path('remove_favorite/<int:course_id>/', views.remove_course_from_favorites, name='remove_favorite'),
    path('favorites/', views.FavoriteCoursesView.as_view(), name='favorites'),
    path('settings/', views.SettingsFormView.as_view(), name='settings'),
    path('get_certificate/', views.get_certificate_view, name='get_certificate'),
]

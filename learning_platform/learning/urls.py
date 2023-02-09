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
]

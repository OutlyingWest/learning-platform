from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.MainView.as_view(), name='index'),
    path('create/', views.create, name='create'),
    path('delete/<int:course_id>/', views.delete, name='delete'),
    re_path('^detail/(?P<course_id>[1-9]+[0-9]*)/$', views.CourseDetailView.as_view(), name='detail'),
    path('enroll/<int:course_id>/', views.enroll, name='enroll'),
]

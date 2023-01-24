from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create/', views.create, name='create'),
    path('delete/<int:course_id>', views.delete, name='delete'),
    path('detail/<int:course_id>', views.detail, name='detail'),
    path('enroll/<int:course_id>', views.enroll, name='enroll'),
]

from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from .models import Course, Lesson


def index(request):
    courses = Course.objects.all()
    current_year = datetime.now().year
    return render(request,
                  context={
                      'courses': courses,
                      'current_year': current_year,
                  },
                  template_name='index.html')


def create(request):
    return HttpResponse('Форма для создания собственного курса')


def delete(request, course_id):
    return HttpResponse(f'Удаление указанного курса id: {course_id}')


def detail(request, course_id):
    course = Course.objects.get(id=course_id)
    lessons = Lesson.objects.filter(course=course_id)
    context = {
        'course': course,
        'lessons': lessons,
    }
    return render(request,
                  context=context,
                  template_name='detail.html')


def enroll(request, course_id):
    return HttpResponse(f'Здесь можно записаться на выбранный курс id: {course_id}')

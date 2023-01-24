from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse('Список всех доступных курсов')


def create(request):
    return HttpResponse('Форма для создания собственного курса')


def delete(request, course_id):
    return HttpResponse(f'Удаление указанного курса id: {course_id}')


def detail(request, course_id):
    return HttpResponse(f'Детальная информация о курсе id: {course_id}')


def enroll(request, course_id):
    return HttpResponse(f'Здесь можно записаться на выбранный курс id: {course_id}')



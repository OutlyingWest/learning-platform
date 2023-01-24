from django.http import HttpResponse
from django.shortcuts import render


def login(request):
    return HttpResponse('Страница для входа пользователя на сайт')


def register(request):
    return HttpResponse('Страница для регистрации пользователя')


def logout(request):
    return HttpResponse('Это представление выполняет выход и редирект на страницу входа')


def change_password(request):
    return HttpResponse('Этот обработчик меняет пароль пользователя')


def reset_password(request):
    return HttpResponse('Этот обработчик отвечает за сброс пароля пользователя')

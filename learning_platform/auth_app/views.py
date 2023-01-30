from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import HttpResponse
from .models import User


def login(request):
    if request.method == 'POST':
        data = request.POST
        user = auth.authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            auth.login(request, user)
            return redirect('index')
        else:
            return HttpResponse('Ваш аккаунт заблокирован')
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        text_data = request.POST
        if request.FILES:
            file_data = request.FILES
        else:
            file_data = dict(avatar=None)
        user = User(email=text_data['email'],
                    first_name=text_data['first_name'],
                    last_name=text_data['last_name'],
                    birthday=text_data['birthday'],
                    avatar=file_data['avatar'],
                    description=text_data['description'],)
        user.set_password(text_data['password'])
        user.save()
        auth.login(request, user)
        return redirect('index')
    else:
        return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


def change_password(request):
    return HttpResponse('Этот обработчик меняет пароль пользователя')


def reset_password(request):
    return HttpResponse('Этот обработчик отвечает за сброс пароля пользователя')

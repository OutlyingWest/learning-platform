from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib import auth
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from .forms import LoginForm, RegisterForm
from .signals import account_access


class UserLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'login.html'
    next_page = 'index'

    def form_valid(self, form):
        is_remember = self.request.POST.get('is_remember')
        if is_remember == 'on':
            self.request.session[settings.REMEMBER_KEY] = datetime.now().isoformat()
            # Set session lifetime
            self.request.session.set_expiry(settings.SESSION_REMEMBER_AGE)
        elif is_remember == 'off':
            self.request.session.set_expiry(0)

        # Email log in alert message sending
        account_access.send(sender=self.__class__, request=self.request)
        return super(UserLoginView, self).form_valid(form)


class UserRegisterView(CreateView):
    model = settings.AUTH_USER_MODEL
    form_class = RegisterForm
    template_name = 'register.html'

    def form_valid(self, form):
        user = form.save()

        auth.login(self.request, user)
        return redirect('index')


def change_password(request):
    return HttpResponse('Этот обработчик меняет пароль пользователя')


def reset_password(request):
    return HttpResponse('Этот обработчик отвечает за сброс пароля пользователя')

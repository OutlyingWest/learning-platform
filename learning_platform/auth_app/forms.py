from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'birthday', 'description', 'avatar', )


class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('email', 'password', )

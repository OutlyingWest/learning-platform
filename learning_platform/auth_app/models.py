from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from .functions import get_timestamp_path_user


class VarCharField(models.CharField):
    def db_type(self, connection):
        longtext: str = super().db_type(connection)
        varchar: str = longtext.replace('longtext', 'varchar')
        return varchar


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    email = models.EmailField(verbose_name='Email', unique=True)
    birthday = models.DateField(verbose_name='Дата рождения', blank=False, null=True)
    description = VarCharField(verbose_name='Обо мне',
                               max_length=150, blank=True,
                               unique=False,
                               default='',
                               db_index=True)
    avatar = models.ImageField(verbose_name='Фото', blank=True, upload_to=get_timestamp_path_user,
                               validators=[FileExtensionValidator(allowed_extensions=['jpg', 'bmp', 'png'],
                                                                  message='Wrong file format')])
    username = models.CharField(
        max_length=150,
        unique=False,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name_plural = 'Участники'
        verbose_name = 'Участник'
        ordering = ['last_name']

    def __str__(self):
        return f'Участник {self.first_name} {self.last_name}: {self.email}'

from django.conf import settings
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from django.template.loader import render_to_string
from django.utils import timezone

account_access = Signal()


def send_login_user_email(**kwargs):
    template_name = 'registration/account_access_email.html'
    request = kwargs['request']
    context = {
        'request': request,
        'message': f'В ваш аккаунт был выполнен вход {timezone.now().isoformat()}.\n'
                   f'Если вы не совершали это действие, рекомендуется срочно'
    }
    email = EmailMessage(subject='Вход в аккаунт | онлайн платформа',
                         body=render_to_string(template_name, context),
                         to=[request.POST['username']])
    email.content_subtype = 'html'
    email.send(fail_silently=False)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def grant_user_rights(sender, instance, created=True, **kwargs):
    if created:
        pupil = Group.objects.filter(name='Ученик')
        instance.groups.set(pupil)
        print(f'Пользователь {instance} успешно добавлен в группу "Ученик"')


account_access.connect(send_login_user_email)

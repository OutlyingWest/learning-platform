from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from  django.dispatch import receiver


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def grant_user_rights(sender, instance, created=True, **kwargs)
    if created:
        pupil = Group.objects.filter(name='Ученик')
        instance.groups.set(pupil)
        print(f'Пользователь {instance} успешно добавлен в группу "Ученик"')

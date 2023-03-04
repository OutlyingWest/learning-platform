from django.db.models.signals import pre_save
from .models import Course, Lesson


def check_quantity(sender, instance, **kwargs):
    """ Check is lessons quantity set by user at lessons creation equal with quantity defined at Course creation  """
    error = None
    actual_count = sender.objects.filter(course=instance.course).count()
    set_count = Course.objects.filter(id=instance.course.id).values('count_lessons')[0]['count_lessons']

    if actual_count >= set_count:
        error = (f'Количество уроков ограничено ' +
                 f'При создании курса вы установили, что он будет содержать {set_count} уроков.')
    return error


pre_save.connect(check_quantity, sender=Lesson)

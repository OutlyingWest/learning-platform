from django.db.models.signals import pre_save
from django.dispatch import Signal
from .models import Course, Lesson


set_views = Signal()


def check_quantity(sender, instance, **kwargs):
    """ Check is lessons quantity set by user at lessons creation equal with quantity defined at Course creation  """
    error = None
    actual_count = sender.objects.filter(course=instance.course).count()
    set_count = Course.objects.filter(id=instance.course.id).values('count_lessons')[0]['count_lessons']

    if actual_count >= set_count:
        error = (f'Количество уроков ограничено ' +
                 f'При создании курса вы установили, что он будет содержать {set_count} уроков.')
    return error


def increment_views(sender, **kwargs):
    """ Perform getting data about page views """
    session = kwargs['session']
    views: dict = session.setdefault('views', {})
    course_id = str(kwargs['id'])
    count = views.get(course_id, 0)
    views[course_id] = count + 1
    session['views'] = views
    # Send cookies in every request
    session.modified = True


pre_save.connect(check_quantity, sender=Lesson)
set_views.connect(increment_views, )
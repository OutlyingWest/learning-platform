from django.core.mail import send_mail, EmailMultiAlternatives, get_connection, EmailMessage
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.template.loader import render_to_string
from django.dispatch import Signal, receiver
from .models import Course, Lesson


set_views = Signal()
course_enroll = Signal()
get_certificate = Signal()


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


def send_enroll_email(**kwargs):
    template_name = 'emails/course_info_email.html'
    course = Course.objects.get(id=kwargs['course_id'])
    context = {
        'course': course,
        'message': f'Вы были успешно записаны на курс {course.title}.'
                   f'Первый урок будет доступен уже {course.start_date}.'
    }
    send_mail(subject='Запись на курс от онлайн платформы',
              message='',
              from_email=settings.DEFAULT_FROM_EMAIL,
              recipient_list=[kwargs['request'].user.email],
              html_message=render_to_string(template_name, context, kwargs['request']),
              fail_silently=False)


def send_user_certificate(**kwargs):
    template_name = 'emails/certificate_email.html'
    context = {
            'message': 'Поздравляем! Вы успешно закончили курс.\n'
                        'Bo вложении прилагаем сертификат о прохождении'
    }
    email = EmailMultiAlternatives(subject='Сертификат о прохождении курса | Платформа Codeby',
                                   to=[kwargs['sender'].email])
    email.attach_alternative(render_to_string(template_name, context), mimetype='text/html')
    email.attach_file(path=settings.MEDIA_ROOT / 'certificates/certificate.png', mimetype='image/png')
    email.send(fail_silently=True)


@receiver(post_save, sender=Lesson)
def send_info_email(sender, instance, **kwargs):
    """ Multiple mailing to registered users, when new course added """
    if kwargs['created']:
        actual_count = sender.objects.filter(course=instance.course).count()
        set_count = Course.objects.filter(id=instance.course.id).values('count_lessons')[0]['count_lessons']
        if actual_count == set_count:
            template_name = 'emails/course_info_email.html'
            course = Course.objects.get(id=instance.course.id)
            context = {
                          'course': course,
                          'message': f'Hа нешей платформе появился новый куpс {course.title}.\n'
                                     f'Подробную информацию Вы можете получить по ссылке ниже'
            }
            user = get_user_model()

            # Get user's emails list
            recipients = user.objects.exclude(is_staff=True).values_list('email', flat=True)
            # Create connection with smtp server
            connection = get_connection(fail_silently=True)
            # Multiple mailing to registered users
            emails = []
            for email_address in recipients:
                email_message = EmailMessage(subject='Время обучиться новому скиллу | Онлайн платформа',
                                             body=render_to_string(template_name, context),
                                             to=[email_address], connection=connection)
                email_message.content_subtype = 'html'
                emails.append(email_message)
            connection.send_messages(emails)
            connection.close()


pre_save.connect(check_quantity, sender=Lesson)
set_views.connect(increment_views, )
course_enroll.connect(send_enroll_email, )
get_certificate.connect(send_user_certificate, )
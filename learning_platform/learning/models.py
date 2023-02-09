from django.conf import settings
from django.db import models


class Course(models.Model):
    title = models.CharField(verbose_name='Название курса', max_length=30, unique=True)
    author = models.ForeignKey(verbose_name='Автор курса', to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    description = models.TextField(verbose_name='Описание курса', max_length=200)
    start_date = models.DateField(verbose_name='Старт курса')
    duration = models.PositiveIntegerField(verbose_name='Продолжительность')
    price = models.PositiveIntegerField(verbose_name='Цена', blank=True)
    count_lessons = models.PositiveIntegerField(verbose_name='Количество уроков')

    class Meta:
        verbose_name_plural = 'Курсы'
        verbose_name = 'Курс'
        ordering = ['title']
        # Set permissions for model in format: (<codename>, <name>) where field <name> - comment
        permissions = (
            ('modify_course', 'Can modify course content'),
        )

    def __str__(self):
        return f'{self.title}: Старт {self.start_date}'


class Lesson(models.Model):
    course = models.ForeignKey(verbose_name='Курс', to=Course, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Название урока', max_length=25, unique=True)
    preview = models.TextField(verbose_name='Описание урока', max_length=100)

    class Meta:
        verbose_name_plural = 'Уроки'
        verbose_name = 'Урок'
        ordering = ['course']
        permissions = (
            ('modify_lesson', 'Can modify lesson content'),
        )

    def __str__(self):
        return f'{self.course}: Урок {self.name}'


class Tracking(models.Model):
    lesson = models.ForeignKey(verbose_name='Урок', to=Lesson, on_delete=models.PROTECT)
    user = models.ForeignKey(verbose_name='Ученик', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    passed = models.BooleanField(verbose_name='Пройден?', default=None)

    class Meta:
        ordering = ['-user']


class Review(models.Model):
    user = models.ForeignKey(verbose_name='Ученик', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(verbose_name='Курс', to=Course, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='Текст отзыва', max_length=250, unique_for_year='sent_date')
    sent_date = models.DateField(verbose_name='Дата отправки отзыва', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'
        ordering = ['-sent_date']
        unique_together = ('user', 'course', )    # Super key

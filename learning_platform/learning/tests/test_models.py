from django.test import TestCase, tag
from learning.models import Course, Lesson


class LearningModelsTestCase(TestCase):
    fixtures = ['test_data.json']

    @tag('course_to_str')
    def test_course_to_str(self):
        course = Course.objects.get(title='Go')
        self.assertEqual(str(course), f'{course.title}: Старт {course.start_date}')

    @tag('lesson_to_str')
    def test_lesson_to_str(self):
        lesson = Lesson.objects.get(name='1й Go')
        self.assertEqual(str(lesson), f'{lesson.course.title}: Старт {lesson.course.start_date}: Урок {lesson.name}')

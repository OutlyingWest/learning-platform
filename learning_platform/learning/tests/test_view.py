import django
from django.db.models import Q
from django.shortcuts import reverse
from django.test import TestCase, Client

from learning.models import Course, Lesson, Tracking


class LearningViewTestCase(TestCase):
    fixtures = ['test_data.json']

    def setUp(self) -> None:
        self.client = Client()
        self.index = reverse('index')
        self.create = reverse('create')
        self.tracking = reverse('tracking')

    def test_get_index_view(self):
        response = self.client.get(self.index)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(len(response.context['courses']), 2)

    def test_get_index_view_by_page(self):
        response = self.client.get(self.index, data={'page': 1})
        self.assertEqual(len(response.context['courses']), 2)

    def test_search_and_order_by_view(self):
        search_query = {'search': 'h', 'price_order': '-price'}

        response = self.client.get(self.index, data=search_query)
        filters = Q(title＿_contains=search_query['search']) | Q(description__icontains=search_query['search'])
        courses = Course.objects.filter(filters).order_by(search_query['price_order'])
        self.assertEqual(len(response.context['courses']), len(courses))
        self.assertQuerysetEqual(response.context['courses'], courses)

    def test_get_detail_view(self):
        for course_id in Course.objects.values_list('id', flat=True):
            response = self.client.get(reverse('detail', kwargs={'course_id': course_id}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detail.html')
        self.assertEqual(len(response.context['lessons']),
                         Lesson.objects.filter(course=course_id).count())

    def test_get_create_view_not_login(self):
        response = self.client.get(path=self.create)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + self.create, status_code=302)

    def test_get_create_view_not_permission_add_course(self):
        login = self.client.login(username='alexeybuv@yandex.ru', password='student1234')

        response = self.client.get(self.create)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'errors/403.html')

    def test_get_create_view(self):
        login = self.client.login(username='alexeybuv7@gmail.com', password='123450')

        response = self.client.get(self.create)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create.html')

    def test_post_create_view(self):
        login = self.client.login(username='alexeybuv7@gmail.com', password='123450')

        response = self.client.post(self.create, data={
            'title': 'Python Pro',
            'description': 'Oписание',
            'start_date': django.utils.timezone.now().date().isoformat(),
            'duration': 3,
            'price': 31000,
            'count_lessons': 15
        })
        course = Course.objects.get(title='Python Pro')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse('create_lesson', kwargs={'course_id': course.id}),
                             status_code=302)

    def test_get_setting_view(self):
        response = self.client.get(reverse('settings'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings.html')

    def test_post_setting_view(self):
        response = self.client.post(reverse('settings'), data={'paginate_by': 2})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index, status_code=302)
        self.assertEqual(self.client.cookies.get('paginate_by').value, '2')
        response_index = self.client.get(self.index)
        self.assertEqual(len(response_index.context['courses']), 2)

    def test_get_review_view(self):
        login = self.client.login(username='alexeybuv@yandex.ru', password='student1234')

        course = Course.objects.get(title='Go')
        response = self.client.get(reverse('review', kwargs={'course_id': course.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review.html')

    def test_post_review_view(self):
        login = self.client.login(username='alexeybuv@yandex.ru', password='student1234')

        course = Course.objects.get(title='PHP')
        response_get = self.client.get(reverse('review', kwargs={'course_id': course.id}))
        response = self.client.post(reverse('review', kwargs={'course_id': course.id}),
                                    data={
                                        'content': 'Курс очень понравился',
                                        'course': course,
                                        'user': response_get.context['user'],
                                    })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('detail', kwargs={'course_id': course.id}), status_code=302)

    def test_add_add_to_favourites(self):
        courses_ids = Course.objects.filter(id__in=[1, 3]).values_list('id', flat=True)

        for course_id in courses_ids:
            response = self.client.post(reverse('add_booking', kwargs={'course_id': course_id}))
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, self.index, status_code=302)
            self.assertIn(course_id, self.client.session.get('favourites'))

    def test_add_remove_favourites(self):
        session = self.client.session

        session['favourites'] = [1, 3]
        session.save()
        response = self.client.post(reverse('remove_booking', kwargs={'course_id': 5}))
        self.assertEqual(len(self.client.session.get('favourites')), 3)
        self.assertRedirects(response, self.index, status_code=302)
        self.assertNotIn(5, self.client.session.get('favourites'))

    def test_get_favourites(self):
        session = self.client.session

        session['favourites'] = [2, 4]
        session.save()
        response = self.client.get(reverse('favourites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(len(response.context['courses']), len(session['favourites']))

    def test_enroll_view(self):
        login = self.client.login(username='alexeybuv@yandex.ru', password='student1234')

        course = Course.objects.last()
        response = self.client.post(reverse('enroll',
                                            kwargs={'course_id': course.id}))
        self.assertRedirects(response, self.tracking, status_code=302)
        self.assertEqual(Tracking.objects.filter(user=response.context['user'], lesson__course=course.id).count(),
                         Lesson.objects.filter(course=course).count())
        response = self.client.post(reverse('enroll', kwargs={'course_id': course.id}))
        self.assertEqual(str(response.content, 'utf-8'), 'Вы уже записаны на данный курс')

    def test_course_delete_view(self):
        login = self.client.login(username='alexeybuv7@gmail.com', password='123450')

        course = Course.objects.get(title='PHP')
        response = self.client.post(reverse('delete', kwargs={'course_id': course.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index)

    def test_course_update_view(self):
        login = self.client.login(username='alexeybuv7@gmail.com', password='123450')

        course = Course.objects.last()
        response = self.client.post(reverse('update', kwargs={'course_id': course.id}), data={
            'title': course.title,
            'description': course.description,
            'start_date': course.start_date,
            'duration': course.duration,
            'price': course.price + 1500,
            'count_lessons': course.count_lessons + 3,
        })
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(course.count_lessons, Course.objects.get(id=course.id).count_lessons)

    def test_lesson_create_view(self):
        self.client.login(username='alexeybuv7@gmail.com', password='123450')

        course = Course.objects.get(title='Django&DRF')
        response_1 = self.client.post(reverse('create_lesson', kwargs={'course_id': course.id}), data={
            'course': course.id,
            'name': 'Последний урок курса',
            'preview': 'Описание урока',
        })
        self.assertEqual(response_1.status_code, 302)
        response_2 = self.client.post(reverse('create_lesson', kwargs={'course_id': course.id}), data={
            'course': course.id,
            'name': 'Последний урок',
            'preview': 'Описание',
        })
        self.assertEqual(response_2.status_code, 200)
        self.assertFormError(response_2, 'form', field=None,
                             errors=f'количество уроков ограничено! Ранее вы установили, '
                                    f'что курс будет содержать {course.count_lessons} уроков')

    def test_get_certificate_view(self):
        login = self.client.login(username='alexeybuv@yandex.ru', password='student1234')

        course = Course.objects.first()
        response_1 = self.client.post(reverse('enroll', kwargs={'course_id': course.id}))

        response_2 = self.client.post(reverse('get_certificate', kwargs={'course_id': course.id}))
        self.assertEqual(str(response_2.content, 'utf-8'), 'Вы не прoшли кypс полностью')

        Tracking.objects.filter(user=response_1.context['user'], lesson__course=course.id).update(passed=True)
        response_3 = self.client.post(reverse('get_certificate', kwargs={'course_id': course.id}))
        self.assertEqual(str(response_3.content, 'utf-8'), 'Сертификат отправлен на Ваш email')




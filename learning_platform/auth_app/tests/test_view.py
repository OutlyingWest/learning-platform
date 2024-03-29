from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.conf import settings
from django.test import TestCase, Client
from django.shortcuts import reverse
from django.utils import timezone


class AuthAppTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создание группы с правами "Ученик"
        cls.student_group = Group.objects.create(name='Ученик')
        cls.student_perms = Permission.objects.filter(
            content_type__app_label='learning',
            codename__in=['view', 'add_tracking']
        )
        cls.student_group.permissions.set(cls.student_perms)

    def setUp(self) -> None:
        self.user_valid_register_data = {
            'username': 'alex',
            'email': 'alexeybuv@yandex.ru',
            'description': '',
            'birthday': timezone.now().date(),
            'password': 'student1234',
        }
        self.user_invalid_register_data = {
            'username': 'alexeybuv@yandex.ru',
            'birthday': timezone.now().date(),
            'description': '',
            'password': 'student4321'
        }
        self.user_login_data_with_remember = {
            'username': 'alexeybuv@yandex.ru',
            'password': 'student1234',
            'is_remember': 'on'
        }
        self.user_login_data_without_remember = {
            'username': 'alexeybuv@yandex.ru',
            'password': 'student1234',
            'is_remember': 'off'
        }
        self.invalid_login_data = {
            'username': ' example@example.com',
            'password': 'admin1234',
        }
        self.admin = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin12345',

        )
        self.client = Client()
        self.register = reverse('register')
        self.login = reverse('login')
        self.logout = reverse('logout')
        self.index = reverse('index')

    def test_get_register_view(self):
        response = self.client.get(path=self.register)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_post_register_view(self):
        response = self.client.post(path=self.register, data=self.user_valid_register_data)
        self.assertEqual(response.status_code, 200)

    def test_post_register_view_with_email_existed(self):
        get_user_model().objects.create_user(**self.user_valid_register_data)

        response = self.client.post(path=self.register, data=self.user_valid_register_data)
        self.assertFormError(response, 'form', 'email', 'Участник с таким Email уже существует.')

    def test_get_login_view(self):
        response = self.client.get(path=self.login)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_post_login_view_with_remember(self):
        get_user_model().objects.create_user(**self.user_valid_register_data)

        response = self.client.post(path=self.login, data=self.user_login_data_with_remember)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session.get_expiry_age(), settings.SESSION_REMEMBER_AGE)
        response_index = self.client.get(self.index)
        self.assertTrue(response_index.context['user'].is_authenticated)

    def test_post_login_view_without_remember(self):
        get_user_model().objects.create_user(**self.user_valid_register_data)

        response = self.client.post(path=self.login, data=self.user_login_data_without_remember)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session.get_expiry_age(), settings.SESSION_COOKIE_AGE)
        response_index = self.client.get(self.index)
        self.assertTrue(response_index.context['user'].is_authenticated)

    def test_logout_view(self):
        response = self.client.post(self.logout)
        self.assertEqual(response.status_code, 302)

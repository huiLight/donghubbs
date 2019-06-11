from django.test import TestCase
from django.urls import reverse
from django.urls import resolve
from donghu.views import user_login
from django.contrib.auth.models import User
from django.utils import timezone

class LoginTest(TestCase):
    def setUp(self):
        # 每次测试都会在一个新的环境进行，所以要先创建用户
        u = User.objects.create(username='test', password='test12345', email='123@test.com',is_superuser=1, first_name=' ', last_name=' ', is_staff=1,is_active=1, date_joined=timezone.now())
        u.set_password('test12345')
        u.save()

    def test_root_url_resolves_to_user_login_view(self):
        found = resolve('/')
        self.assertEqual(found.func, user_login)

    def test_notlogin_index(self):
        """
            If user has not login, show the login view.
        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'donghu/login.html')

    def test_login_index(self):
        """
            If user has logined, redirect to the index page.
        """
        self.client.login(username='test', password='test12345')

        response = self.client.get('/')
        self.assertRedirects(response, '/index/')

class IndexTest(TestCase):

    def test_module(self):
        pass
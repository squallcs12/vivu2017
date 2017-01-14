from django.conf import settings


from accounts.factories.user_factory import UserFactory
from common.tests.core import TestCase


class AccountLoginTestCase(TestCase):
    def test_show_login_view(self):
        self.visit(settings.LOGIN_URL)
        self.should_see_text('If you have not created an account yet, then please')
        self.assertTrue(self.find('label[for="id_login"]'))
        self.assertTrue(self.find('label[for="id_password"]'))

    def test_login_without_username(self):
        user = UserFactory()
        response = self.client.post(settings.LOGIN_URL, {
            'auth-username': '',
            'auth-password': user.raw_password,
            'login_view-current_step': 'auth'
        })
        self.assertEqual(response.status_code, 200)
        self.set_response(response)
        self.should_see_text('This field is required')

    def test_login_without_password(self):
        user = UserFactory()
        response = self.client.post(settings.LOGIN_URL, {
            'auth-username': user.username,
            'auth-password': '',
            'login_view-current_step': 'auth'
        })
        self.assertEqual(response.status_code, 200)
        self.set_response(response)
        self.should_see_text('This field is required')

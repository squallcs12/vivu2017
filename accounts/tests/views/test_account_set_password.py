from django.conf.urls import url
from django.contrib.auth import login
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.test.utils import override_settings


from common.tests.core import TestCase
from accounts.factories.user_factory import UserFactory


class AccountSetPasswordTestCase(TestCase):
    @classmethod
    def fake_login_view(cls, request):
        user = cls.user
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return HttpResponse(request.user.username)

    def fake_login(self, user):
        AccountSetPasswordTestCase.user = user
        with override_settings(ROOT_URLCONF=__name__):
            self.visit('/log_to_my_user')

    def setUp(self):
        self.user = UserFactory.build()
        self.user.password = ''
        self.user.save()

        self.fake_login(self.user)

    def fill_new_password(self, password, confirm_password):
        response = self.client.post(reverse('account_set_password'), {
            'password1': password,
            'password2': confirm_password,
        })
        self.set_response(response)

    def test_valid_password(self):
        self.fill_new_password('abcABC123!', 'abcABC123!')
        self.assertEqual(self.response.status_code, 302)

    def test_weak_password(self):
        self.fill_new_password('abc', 'abc')

        self.assertEqual(self.response.status_code, 200)
        self.should_see_text('Password must be a minimum of 6 characters.')

    def test_not_match_password(self):
        self.fill_new_password('abc123', '123456')

        self.assertEqual(self.response.status_code, 200)
        self.should_see_text('You must type the same password each time.')


urlpatterns = [
    url(r'^log_to_my_user', AccountSetPasswordTestCase.fake_login_view, name='login_view'),
]

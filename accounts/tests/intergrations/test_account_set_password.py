from django.conf.urls import url
from django.contrib.auth import login
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.test.utils import override_settings

from common.tests.core import BaseLiveTestCase
from common.tests.factories.user_factory import UserFactory


class AccountSetPasswordTestCase(BaseLiveTestCase):
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
        return self.user

    def fill_new_password(self, password, confirm_password):
        self.visit(reverse('accounts:set_user_password'))

        self.fill_in('#id_new_password1', password)
        self.fill_in('#id_new_password2', confirm_password)
        self.find('#set-password-btn').click()

    def test_valid_password(self):
        self.fill_new_password('abcABC123!', 'abcABC123!')
        self.should_see_text('Password set successful')

    def test_weak_password(self):
        self.fill_new_password('abc', 'abc')
        self.should_see_text('This password is too short. It must contain at least 8 characters.')

    def test_not_match_password(self):
        self.fill_new_password('abc', '123')
        self.should_see_text('The two password fields didn\'t match.')

urlpatterns = [
    url(r'^log_to_my_user', AccountSetPasswordTestCase.fake_login_view, name='login_view'),
]

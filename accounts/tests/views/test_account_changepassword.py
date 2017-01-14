from django.core.urlresolvers import reverse

from common.tests.core import TestCase


class AccountChangePasswordTestCase(TestCase):
    def setUp(self):
        self.login_user()

    def submit_change_password_form(self, old_pw, new_pw, confirm_pw):
        response = self.client.post(reverse('account_change_password'), {
            'oldpassword': old_pw,
            'password1': new_pw,
            'password2': confirm_pw,
        }, follow=True)
        self.set_response(response)

    def test_show_change_password_link(self):
        self.visit(reverse('accounts:profile'))
        self.assertEqual(reverse('account_change_password'), self.link('Change password').attrs['href'])

    def test_wrong_old_password(self):
        self.submit_change_password_form('invalid', '123', '123')
        self.should_see_text('Please type your current password.')

    def assert_password_validation(self, password, confirm_password, message):
        self.submit_change_password_form(self.user.raw_password, password, confirm_password)
        self.should_see_text(message)

    def test_new_password_not_match(self):
        self.assert_password_validation('abcABC123!', 'abcABC', 'You must type the same password each time.')

    def test_new_password_weak(self):
        self.assert_password_validation('123', '123', 'Password must be a minimum of 6 characters.')

    def test_change_password_success(self):
        self.assert_password_validation('abcdABC123!', 'abcdABC123!', 'Password successfully changed.')

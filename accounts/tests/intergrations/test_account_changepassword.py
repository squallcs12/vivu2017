from django.core.urlresolvers import reverse

from common.tests.core import BaseLiveTestCase


class AccountChangePasswordTestCase(BaseLiveTestCase):
    def setUp(self):
        self.login_user()

    def submit_change_password_form(self, old_pw, new_pw, confirm_pw):
        self.fill_in('#id_old_password', old_pw)
        self.fill_in('#id_new_password1', new_pw)
        self.fill_in('#id_new_password2', confirm_pw)
        self.button('Change password').click()

    def test_show_changepassword_view(self):
        self.visit(reverse('accounts:profile'))
        self.link('Expand all').click()
        self.link('Change password').click()

        self.until(lambda: self.assertIn(reverse('password_change'), self.browser.current_url))
        self.should_see_text('Change password')

    def test_wrong_old_password(self):
        self.visit(reverse('password_change'))

        self.submit_change_password_form('invalid', '123', '123')
        self.should_see_text('Your old password was entered incorrectly. Please enter it again.')

    def test_new_password_not_match(self):
        self.visit(reverse('password_change'))

        self.submit_change_password_form(self.user.raw_password, 'abcABC123!', 'abcABC')
        self.should_see_text('The two password fields didn\'t match.')

    def test_new_password_weak(self):
        self.visit(reverse('password_change'))

        self.submit_change_password_form(self.user.raw_password, 'abc123', 'abc123')
        self.should_see_text('This password is too short. It must contain at least 8 characters.')

    def test_change_password_success(self):
        self.visit(reverse('password_change'))

        self.submit_change_password_form(self.user.raw_password, 'abcdABC123!', 'abcdABC123!')

        self.until(lambda: self.assertIn(reverse('password_change_done'), self.browser.current_url))
        self.should_see_text('Password change successful')

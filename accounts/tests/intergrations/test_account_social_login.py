from django.core.urlresolvers import reverse

from common.tests.core import BaseLiveTestCase


class AccountSocialLoginTestCase(BaseLiveTestCase):
    def test_login_facebook(self):
        fb_test_account = {
            'email': 'tamhuynh_fiqxsft_test@tfbnw.net',
            'password': 'abcABC123!',
            'name': 'TamHuynh test',
        }

        self.visit(reverse('login'))
        self.find('#facebook').click()

        self.until(lambda: self.assertIn('facebook', self.browser.current_url))
        self.fill_in('#email', fb_test_account['email'])
        self.fill_in('#pass', fb_test_account['password'])
        self.find('#loginbutton').click()

        self.until(lambda: self.should_see_text('Password set'))

    def test_login_google(self):
        self.visit(reverse('login'))
        self.find('#google').click()
        self.until(lambda: self.assertIn('google', self.browser.current_url))

        self.should_see_text('Sign in with your Google Account')

    def test_twitter(self):
        self.visit(reverse('login'))
        self.find('#twitter').click()
        self.until(lambda: self.assertIn('twitter', self.browser.current_url))

        self.should_see_text('Authorize')

from django.core.urlresolvers import reverse

from common.tests.core import BaseLiveTestCase


class AccountSocialLoginTestCase(BaseLiveTestCase):
    def setUp(self):
        self.visit_login_page()

    def test_login_facebook(self):
        self.find('#facebook').click()
        self.until(lambda: self.assertIn('facebook', self.browser.current_url))

        self.find('#loginbutton').should.be.ok

    def test_login_google(self):
        self.find('#google').click()
        self.until(lambda: self.assertIn('google', self.browser.current_url))

        self.should_see_text('Sign in with your Google Account')

    def test_twitter(self):
        self.find('#twitter').click()
        self.until(lambda: self.assertIn('twitter', self.browser.current_url))

        self.should_see_text('Authorize')

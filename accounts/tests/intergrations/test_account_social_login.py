from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

from common.tests.core import BaseLiveTestCase


class AccountSocialLoginTestCase(BaseLiveTestCase):
    def setUp(self):
        self.visit_login_page()

    @classmethod
    def setUpClass(cls):
        with cls.in_environment(DJANGO_LIVE_TEST_SERVER_ADDRESS='localhost:8180'):
            super(AccountSocialLoginTestCase, cls).setUpClass()

    def init_social_app(self, provider):
        provider_upper = provider.upper()
        site = Site.objects.get()
        app = SocialApp.objects.create(provider=provider, name=provider,
                                       client_id=self.env('AUTH_{}_KEY'.format(provider_upper)),
                                       secret=self.env('AUTH_{}_SECRET'.format(provider_upper)))
        app.sites.add(site)

    def test_login_facebook(self):
        self.init_social_app(provider='facebook')

        self.find('#facebook').click()
        self.until(lambda: 'facebook.com' in self.browser.current_url)

        self.find('#loginbutton').should.be.ok

    def test_login_google(self):
        self.init_social_app(provider='google')

        self.find('#google').click()
        self.until(lambda: 'google.com' in self.browser.current_url)

        self.should_see_text('Sign in with your Google Account')

    def test_twitter(self):
        self.init_social_app(provider='twitter')

        self.find('#twitter').click()
        self.until(lambda: 'twitter.com' in self.browser.current_url)

        self.should_see_text('Authorize')

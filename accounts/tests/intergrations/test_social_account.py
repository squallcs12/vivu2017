from django.core.urlresolvers import reverse

from common.tests.core import BaseLiveTestCase
from common.tests.factories.user_social_factory import UserSocialAuthFactory


class SocialAccountTestCase(BaseLiveTestCase):
    def visit_social_list_view(self):
        self.visit(reverse('accounts:profile'))
        if not self.link('Social account').is_displayed():
            self.link('Expand all').click()
            self.until(lambda: self.link('Social account').is_displayed())
        self.link('Social account').click()
        self.until(lambda: self.assertIn(reverse('accounts:social_list'), self.browser.current_url))

    def link_new_social_account(self):
        self.login_user()
        self.visit_social_list_view()
        self.link('Add social account').click()

    def test_show_social_view(self):
        self.login_user()
        self.visit_social_list_view()
        self.should_see_text('Social accounts')

    def test_button_add_social_account(self):
        self.link_new_social_account()
        self.until_current_url_contains(self.settings.LOGIN_URL)

    def test_show_social_account_list(self):
        self.login_user()
        social_accounts = UserSocialAuthFactory.create_batch(3, user=self.user)
        self.visit_social_list_view()
        for account in social_accounts:
            self.should_see_text(account.uid)

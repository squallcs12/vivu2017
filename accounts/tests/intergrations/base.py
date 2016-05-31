from django.core.urlresolvers import reverse

from common.tests.core import BaseLiveTestCase


class AccountTestBase(BaseLiveTestCase):
    def visit_profile(self):
        self.visit(reverse('accounts:profile'))

    def click_account_menu_item(self, text):
        if not self.link(text).is_displayed():
            self.link('Expand all').click()
            self.until(lambda: self.link(text).is_displayed())
        self.link(text).click()

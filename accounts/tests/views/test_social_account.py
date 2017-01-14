from django.core.urlresolvers import reverse

from common.tests.core import TestCase


class SocialAccountTestCase(TestCase):
    def test_show_social_view(self):
        self.login_user()
        self.visit(reverse('socialaccount_connections'))
        self.should_see_text('Account Connections')

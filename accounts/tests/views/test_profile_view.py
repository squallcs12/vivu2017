from django.core.urlresolvers import reverse

from common.tests.core import TestCase
from accounts.factories.user_factory import UserFactory


class ProfileViewTests(TestCase):
    def test_show_correct_information(self):
        user = UserFactory()
        self.login(user)
        keys = ['email', 'username', 'first-name', 'last-name']
        response = self.client.get(reverse('accounts:profile'))

        self.set_response(response)

        for key in keys:
            user_key = key.replace('-', '_')
            self.assertEqual(self.find('.row-data-{}'.format(key)).text, getattr(user, user_key))

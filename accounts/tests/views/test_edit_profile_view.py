from django.urls.base import reverse


from accounts.factories.user_factory import UserFactory
from common.tests.core import TestCase


class EditProfileViewTests(TestCase):
    def setUp(self):
        user = UserFactory()

        self.login(user)
        self.user = user

    def test_add_valid_information(self):
        keys = [
            'first_name',
            'last_name',
        ]
        expected_user = UserFactory.build()

        data = dict([(x, getattr(expected_user, x)) for x in keys])
        response = self.client.post(reverse('accounts:edit_profile'), data)
        self.assertEqual(response.status_code, 302)

        self.user.refresh_from_db()
        for k in keys:
            self.assertEqual(getattr(self.user, k), getattr(expected_user, k))

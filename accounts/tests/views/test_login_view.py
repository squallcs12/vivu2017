from django.conf import settings
from django.urls.base import reverse


from common.tests.core import TestCase


class LoginViewTests(TestCase):
    def process_login(self, user):
        return self.client.post(settings.LOGIN_URL, {
            'login': user.username,
            'password': user.raw_password,
        })

    def test_user_asked_for_verify_email_after_login(self):
        user = self.init_user(verified=False)

        response = self.process_login(user)

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('account_email_verification_sent'), response['location'])

    def test_user_redirect_to_profile(self):
        user = self.init_user()

        response = self.process_login(user)

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('accounts:profile'), response['location'])

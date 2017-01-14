from django.urls.base import reverse


from common.tests.core import TestCase
from accounts.factories.user_factory import UserFactory


class SignUpViewTests(TestCase):
    def test_fail_used_email(self):
        user = UserFactory()
        response = self.client.post(reverse('account_signup'), {
            'email': user.email
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('A user is already registered with this e-mail address.', response.content.decode())

    def test_signup_success(self):
        user = UserFactory.build()
        response = self.client.post(reverse('account_signup'), {
            'username': user.username,
            'email': user.email,
            'password1': user.raw_password,
            'password2': user.raw_password,
        })

        self.assertEqual(response.status_code, 302)

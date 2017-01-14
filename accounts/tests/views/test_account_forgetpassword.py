from django.core import mail
from django.core.urlresolvers import reverse


from common.tests.core import TestCase
from accounts.factories.user_factory import UserFactory


class AccountForgetPasswordTestCase(TestCase):
    def submit_forgetpassword_email(self, email):
        self.response = self.client.post(reverse('account_reset_password'), {
            'email': email
        })

    def test_show_forgetpassword_view(self):
        self.visit(reverse('account_reset_password'))
        self.should_see_text('Password Reset')
        self.assertTrue(self.find('label[for="id_email"]'))

    def test_invalid_email(self):
        invalid_email = [
            'abc'
            'abc@'
            'abc@d'
            '@abc'
        ]

        for email in invalid_email:
            self.submit_forgetpassword_email(email)
            self.assertEqual(self.response.status_code, 200)
            self.should_see_text('Enter a valid email address')

    def test_valid_unregistered_email(self):
        self.submit_forgetpassword_email('abc@xyz.com')
        self.assertEqual(self.response.status_code, 200)
        self.should_see_text('The e-mail address is not assigned to any user account')

    def test_valid_registered_email(self):
        user = UserFactory()
        self.submit_forgetpassword_email(user.email)

        self.assertEqual(self.response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Password Reset', mail.outbox[0].subject)

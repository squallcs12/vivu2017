from django.core.urlresolvers import reverse

from common.tests.core import BaseLiveTestCase
from django.core import mail
from common.tests.factories.user_factory import UserFactory


class AccountForgetPasswordTestCase(BaseLiveTestCase):
    def submit_forgetpassword_email(self, email):
        self.fill_in('#id_email', email)
        self.button('Reset password').click()

    def test_show_forgetpassword_view(self):
        self.visit(reverse('login'))
        self.link('Forgot your password?').click()

        self.until(lambda: self.assertIn(reverse('password_reset'), self.browser.current_url))
        self.should_see_text('Reset password')
        self.assertIsNotNone(self.label('Email'))

    def test_invalid_email(self):
        self.visit(reverse('password_reset'))
        invalid_email = [
            'abc'
            'abc@'
            'abc@d'
            '@abc'
        ]

        for email in invalid_email:
            self.submit_forgetpassword_email(email)
            # The page is not redirect
            self.assertIn(reverse('password_reset'), self.browser.current_url)

    def test_valid_unregistered_email(self):
        self.visit(reverse('password_reset'))
        self.submit_forgetpassword_email('abc@xyz.com')

        self.until(lambda: self.assertIn(reverse('password_reset_done'), self.browser.current_url))
        self.should_see_text('Email sent')

        mail.outbox.should.be.empty

    def test_valid_registered_email(self):
        self.visit(reverse('password_reset'))
        user = UserFactory()
        self.submit_forgetpassword_email(user.email)

        self.until(lambda: self.assertIn(reverse('password_reset_done'), self.browser.current_url))
        self.should_see_text('Email sent')

        mail.outbox.should.have.length_of(1)
        mail.outbox[0].subject.should.contain('Password reset')

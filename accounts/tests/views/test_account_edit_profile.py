from django.conf import settings
from django.core.urlresolvers import reverse


from accounts.factories.user_factory import UserFactory
from common.tests.core import TestCase


class AccountEditProfile(TestCase):
    def test_visit_profile_without_login(self):
        self.visit(reverse('accounts:edit_profile'))
        self.assertEqual(self.response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), self.response['location'])

    def visit_edit_profile(self):
        self.login_user()
        self.visit(reverse('accounts:edit_profile'))

    def test_show_edit_profile_view(self):
        self.visit_edit_profile()
        self.should_see_text('Edit profile')

    def test_show_initial_profile(self):
        self.visit_edit_profile()

        self.assertEqual(self.find('#id_email').attrs['value'], self.user.email)
        self.assertEqual(self.find('#id_first_name').attrs['value'], self.user.first_name)
        self.assertEqual(self.find('#id_last_name').attrs['value'], self.user.last_name)

    def test_change_invalid_email(self):
        self.login_user()

        invalid_emails = ['abc@xyz', 'abc', 'xyz.com', ]

        for email in invalid_emails:
            response = self.client.post(reverse('accounts:edit_profile'), {
                'email': email,
            }, follow=True)
            self.set_response(response)

            self.assertEqual(response.status_code, 200)
            self.should_see_text('Enter a valid email address.')

    def test_change_valid_profile(self):
        self.login_user()
        new_user = UserFactory.build()
        response = self.client.post(reverse('accounts:edit_profile'), {
            'email': new_user.email,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
        })
        self.assertEqual(response.status_code, 302)

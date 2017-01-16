from rest_framework import status

from common.tests.core import TestCase


class HomeViewTestCases(TestCase):
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

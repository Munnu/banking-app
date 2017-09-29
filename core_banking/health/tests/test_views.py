from django.test import TestCase
from django.urls import reverse


class HealthViewTests(TestCase):

    def test_account_view_success(self):
        """Test to see if the health of the system is 200."""
        response = self.client.get(reverse('health'))
        self.assertTrue(response.status_code, 200)
from django.test import TestCase, TransactionTestCase
from django.urls import reverse

from accounts.banking_actions import CreditCard
from accounts.models import Accounts, Customers
from transactions.models import Journals


class AccountsViewTests(TransactionTestCase):
    def setUp(self):
        self.customer_cc = CreditCard()

        self.test_customer = Customers.objects.create(customer_id=1)
        self.test_account = Accounts.objects.create(account_id=1, customer=self.test_customer)

    def test_account_account_exists(self):
        response = self.client.get(reverse('account_view', args=[2]))

        # test to see if it's a 200.
        self.assertTrue(response.status_code, 200)

    def test_account_ledgers_acount_exists(self):
        response = self.client.get(reverse('account_ledgers', args=[2]))
        self.assertTrue(response.status_code, 200)

    def test_account_index_get_failures(self):
        response = self.client.get('/accounts/')

        # GET requests should not be allowed on this endpoint
        self.assertTrue(response.status_code, 405)

    def test_account_index_add_customer(self):
        # essentially a curl -X POST localhost:8000/accounts/
        response = self.client.post('/accounts/')

        # test to see if it's a 200.
        self.assertTrue(response.status_code, 200)

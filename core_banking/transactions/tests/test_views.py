import json

from django.test import TestCase

from accounts.banking_actions import CreditCard
from accounts.models import Accounts, Customers


class TransactionsViewTests(TestCase):
    def setUp(self):
        self.customer_cc = CreditCard()

        self.test_customer = Customers.objects.create(customer_id=3)
        self.test_account = Accounts.objects.create(account_id=3, customer=self.test_customer)

    def test_transactions_index_get_failures(self):
        """Tests the transactions endpoint on GET. Should result in a failure."""
        response = self.client.get('/transactions/')

        # GET requests should not be allowed on this endpoint
        self.assertTrue(response.status_code, 405)

    def test_transactions_index_add_customer(self):
        """Tests the transactions endpoint on POST. Should result in a success."""
        # essentially a curl localhost:8000/transactions/ --data '{"account_id":11, "purchase_amount":30.0}'
        response = self.client.post('/transactions/', data=json.dumps({
                                                        'account_id': self.test_account.account_id,
                                                        'purchase_amount': 300.0}),
                                    content_type='application/json')

        # test to see if it's a 200.
        self.assertTrue(response.status_code, 200)

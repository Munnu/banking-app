from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

from accounts.banking_actions import CreditCard
from accounts.models import Accounts, Customers
from transactions.models import Journals


class BankingTransactionTestCase(TestCase):
    def setUp(self):
        self.customer_cc = CreditCard()

        self.test_customer = Customers.objects.create(customer_id=2)
        self.test_account = Accounts.objects.create(account_id=2, customer=self.test_customer)
        self.test_journal_purchase = Journals.objects.create(transaction_id=4, account=self.test_account)
        self.test_journal_payment = Journals.objects.create(transaction_id=5, transaction_type="payment",
                                                            account=self.test_account)

    def test_add_customer(self):
        account_number = self.customer_cc.add_customer()

        # check to see if you get an integer back
        self.assertIsInstance(account_number['account_id'], int)

    # ====================================================
    def test_get_account_ledgers(self):
        account_ledger = self.customer_cc.get_account_ledgers(self.test_account.account_id)

        # check to see if the dictionary has one of the expected fields
        dict_key_exist = 'principal' in account_ledger
        self.assertTrue(dict_key_exist, True)

    def test_get_account_ledgers_account_doesnt_exist(self):
        account_id = 200  # this account should not exist
        account_ledger = self.customer_cc.get_account_ledgers(account_id)

        # check to see if the dictionary has one of the expected fields
        self.assertTrue(account_ledger["error"], "Transaction couldn't be processed")

    def test_get_account_ledgers_garbage_account_param(self):
        # check to see if the dictionary has one of the expected fields
        with self.assertRaises(ValueError):
            self.customer_cc.get_account_ledgers("Not even a proper account id")

    # ====================================================
    def test_get_account_data(self):
        account_data = self.customer_cc.get_account_data(self.test_account.account_id)
        # check to see if the dictionary has one of the expected fields
        dict_key_exist = ('principal' in account_data) and ('transactions' in account_data)
        self.assertTrue(dict_key_exist, True)

    def test_get_account_data_account_doesnt_exist(self):
        account_id = 200  # this account should not exist
        account_data = self.customer_cc.get_account_data(account_id)

        # check to see if the dictionary has one of the expected fields
        self.assertTrue(account_data["error"], "Transaction couldn't be processed")

    # ====================================================
    def test_submit_transaction(self):
        purchase_amount = 20
        account_transaction = self.customer_cc.submit_transaction(
                                                                  self.test_account.account_id,
                                                                  purchase_amount)
        dict_key_exist = ('transaction_id' in account_transaction) and ('purchase_amount' in account_transaction)
        self.assertTrue(dict_key_exist, True)

    def test_submit_transaction_account_doesnt_exist(self):
        account_id = 200  # this account should not exist
        purchase_amount = 10
        account_transaction = self.customer_cc.submit_transaction(
                                                                  account_id,
                                                                  purchase_amount)
        # check to see if the dictionary has one of the expected fields
        self.assertTrue(account_transaction["error"], "Transaction couldn't be processed")
        
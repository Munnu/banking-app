from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers

from models import Customers, Accounts
from transactions.models import Journals


class CreditCard(object):
    TRANSACTION_TYPES = (
        'new account',
        'payment',
        'purchase',
        'refund',
        'bank fee',
    )

    @staticmethod
    def get_account_data(account_id):
        """get_account_data method gets the account_id from the frontend
        then checks to see if the account exists in the database.
        It will return back the outstanding principal of the account and
        any transaction data for the account that exists.
        
        :param account_id
        :type integer
        """
        try:
            # check to see if account exists in the database
            account = Accounts.objects.get(account_id=account_id)

            transactions = []

            # now that account has been found, find all the transactions associated and populate the list
            transactions_query = Journals.objects.filter(account_id=account_id).order_by('-timestamp')
            for transaction in transactions_query:
                assembled_data = {
                                  'transaction_id': transaction.transaction_id,
                                  'transaction_type': transaction.transaction_type,
                                  'timestamp': transaction.timestamp,
                                  'purchase_amount': transaction.purchase_amount
                                  }

                transactions.append(assembled_data)

            # if so, get the existing amount
            account_json = {
                'account_id': account.account_id,
                'principal': account.principal,
                'transactions': transactions
            }
            return account_json
        except ObjectDoesNotExist:
            return {"error": "This account does not exist."}

    @staticmethod
    def submit_transaction(account_id, purchase_amount):
        try:
            # check to see if account exists in the database
            account = Accounts.objects.get(account_id=account_id)

            if account:
                # now that account has been found, find all the transactions associated and populate the list
                transaction_applied = Journals(purchase_amount=purchase_amount, account=account)
                transaction_applied.save()

                account.principal += transaction_applied.purchase_amount
                account.save()
            return {
                'tansaction_id': transaction_applied.transaction_id,
                'purchase_amount': transaction_applied.purchase_amount,
                'principal': account.principal
            }
        except ObjectDoesNotExist:
            return {"error": "Transaction couldn't be processed"}

    @classmethod
    def add_customer(cls):
        new_customer = Customers()
        new_customer.save()

        new_account = Accounts(customer=new_customer)
        new_account.save()

        new_journal = Journals(
            transaction_type=cls.TRANSACTION_TYPES[0],
            customer=new_customer, account=new_account)
        new_journal.save()

        new_account_json = {'account_id': new_account.account_id}
        return new_account_json

    @classmethod
    def get_account_ledgers(cls, account_id):
        try:
            transactions_query = Journals.objects.filter(account_id=account_id).order_by('-timestamp')
            ledgers = {}
            ledgers['cash-out'] = {}
            ledgers['cash-out']['debit'] = []
            ledgers['cash-out']['credit'] = []

            ledgers['principal'] = {}
            ledgers['principal']['debit'] = []
            ledgers['principal']['credit'] = []
            for transaction in transactions_query:
                print "This is transaction_type", transaction.transaction_type
                if transaction.transaction_type == cls.TRANSACTION_TYPES[2]:  # a purchase
                    ledgers['cash-out']['debit'].append(transaction.purchase_amount)
                    ledgers['principal']['credit'].append(transaction.purchase_amount)
                elif transaction.transaction_type is cls.TRANSACTION_TYPES[1]:  # a payment
                    pass  # ignoring this logic for now since it's not a requirement
            return ledgers
        except ObjectDoesNotExist:
            return {"error": "Transaction couldn't be processed"}

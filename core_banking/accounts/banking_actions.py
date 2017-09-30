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
        
        :returns dictionary containing account_id, account principal, and all account transactions.
        :exception ObjectDoesNotExist
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
        """submit_transaction static method gets the account_id and purchase_amount
        from the frontend then checks to see if the account exists in the database.
        It will create a new transaction entry in the database, and then will return
        the transaction_id, purchase_amount, and account total.

        :param account_id
        :type integer
        
        :param purchase_amount
        :type integer/float
        
        :returns dictionary containing transaction_id, purchase_amount, account principal.
        :exception ObjectDoesNotExist
        """
        try:
            if purchase_amount > 0:  # we will ignore purchases that are 0
                # check to see if account exists in the database
                account = Accounts.objects.get(account_id=account_id)

                if account:
                    # now that account has been found, create a transaction in the database
                    transaction_applied = Journals(purchase_amount=purchase_amount, account=account)
                    transaction_applied.save()

                    account.principal += transaction_applied.purchase_amount
                    account.save()
                    return {
                        'transaction_id': transaction_applied.transaction_id,
                        'purchase_amount': transaction_applied.purchase_amount,
                        'principal': account.principal
                    }
        except ObjectDoesNotExist:
            return {"error": "Transaction couldn't be processed"}

    @classmethod
    def add_customer(cls):
        """add_customer class method creates a new customer and account entry in the database.
        Additionally, a new account transaction will be created in the database.

        :returns dictionary containing the account_id for the newly created customer account.
        """
        new_customer = Customers()
        new_customer.save()

        new_account = Accounts(customer=new_customer)
        new_account.save()

        new_journal = Journals(
            transaction_type=cls.TRANSACTION_TYPES[0],
            account=new_account)
        new_journal.save()

        new_account_json = {'account_id': new_account.account_id}
        return new_account_json

    @classmethod
    def get_account_ledgers(cls, account_id):
        """get_account_ledgers method gets the account_id from the frontend
        then checks to see if there are any transactions inside of the transactions table
        that is associated with the account_id and return the transactions associated if found.

        :param account_id
        :type integer
        
        :returns dictionary containing transaction data
        :exception ObjectDoesNotExist
        """
        try:
            transactions_query = Journals.objects.filter(account_id=account_id).order_by('-timestamp')
            if transactions_query:
                ledgers = {}
                ledgers['account_id'] = account_id
                ledgers['cash_out'] = {}
                ledgers['cash_out']['debit'] = []
                ledgers['cash_out']['credit'] = []

                ledgers['principal'] = {}
                ledgers['principal']['debit'] = []
                ledgers['principal']['credit'] = []
                for transaction in transactions_query:
                    if transaction.transaction_type == cls.TRANSACTION_TYPES[2]:  # a purchase
                        ledgers['cash_out']['debit'].append(transaction.purchase_amount)
                        ledgers['principal']['credit'].append(transaction.purchase_amount)
                return ledgers
            else:
                raise ObjectDoesNotExist({"error": "No Such Account Exists"})
        except ObjectDoesNotExist:
            return {"error": "Transaction couldn't be processed"}

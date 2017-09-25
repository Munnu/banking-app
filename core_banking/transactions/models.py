# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# from accounts.models import Accounts, Customers

class Journals(models.Model):
    """A journal represents all of the transactions for a single account.

    """
    transaction_id = models.AutoField(primary_key=True)
    transaction_type = models.CharField(max_length=20, default="purchase", null=False)
    timestamp = models.DateTimeField(null=False, auto_now_add=True)  # assume transaction happens upon entry
    purchase_amount = models.FloatField(null=False, default=0)
    payment_amount = models.FloatField(null=False, default=0)
    account = models.ForeignKey('accounts.Accounts', null=False)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# from transactions.models import Journals


class Customers(models.Model):
    """Customers model holds identification for the user, 
    this is a future feature
    """
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=30)
    email = models.CharField(max_length=100)


class Accounts(models.Model):
    """Accounts model holds the general account info like user and password.
    An account references to a specific customer
    This is a partial future feature.
    
    """
    account_id = models.AutoField(primary_key=True)
    login_name = models.CharField(max_length=200)
    password = models.CharField(max_length=50)
    principal = models.FloatField(null=False, default=0)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, null=False)

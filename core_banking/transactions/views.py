# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.shortcuts import render

from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.banking_actions import  CreditCard

# from banking_actions import CreditCard

@csrf_exempt
def transactions_process(request):
    """POST request to create a new transaction for the user based on account id."""
    if request.method == 'POST':  # POST is for creating a new account
        request_body = json.loads(request.body)
        account_id = request_body['account_id']
        purchase_amount = request_body['purchase_amount']
        transaction_data = CreditCard.submit_transaction(account_id, purchase_amount)
        response = JsonResponse(transaction_data)

        return response
    else:
        return HttpResponse("GET not available for transactions endpoint.", status=405)  # method not allowed

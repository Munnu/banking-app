# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.http import JsonResponse

from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

from banking_actions import CreditCard


@csrf_exempt  # for now, using csrf_exempt to bypass POST complaint
def account_index(request):  # this will hold the POST response to add a new account entry
    if request.method == 'POST':  # POST is for creating a new account
        # call to create our new entry
        new_credit_card_account = CreditCard.add_customer()
        response = JsonResponse(new_credit_card_account)
        return response
    else:  # GET
        return HttpResponse("No account ID has been provided for %s" % request.method, status=405)  # method not allowed


def account_view(request, account_id):  # this will hold the GET response to show the account at whatever ID
    # call to get an account
    retrieved_account = CreditCard.get_account_data(account_id)
    response = JsonResponse(retrieved_account)
    return HttpResponse(response)


def account_ledgers(request, account_id):
    """Account ledgers will call the method that will 
    apply logic to figure out what ledger should the transaction data go into.
    """
    retrieved_ledgers = CreditCard.get_account_ledgers(account_id)
    return render(request, 'accounts/ledgers.html', retrieved_ledgers)

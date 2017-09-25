# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse(200)  # returns 200 to ensure the server is up and running

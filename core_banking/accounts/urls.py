from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.account_index, name='account_index.'),
    url(r'^(?P<account_id>[0-9]+)/$', views.account_view, name='account_view'),
    url(r'^(?P<account_id>[0-9]+)/ledgers/$', views.account_ledgers, name='account_ledgers'),
]

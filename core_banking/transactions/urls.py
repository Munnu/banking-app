from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.transactions_process, name='transaction processing.'),
]
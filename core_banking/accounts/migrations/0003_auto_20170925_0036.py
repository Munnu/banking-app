# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 00:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20170924_2120'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accounts',
            old_name='customer_id',
            new_name='customer',
        ),
    ]

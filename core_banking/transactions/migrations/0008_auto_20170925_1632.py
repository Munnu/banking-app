# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 16:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0007_auto_20170925_0446'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='journals',
            name='customer',
        ),
        migrations.AlterField(
            model_name='journals',
            name='transaction_type',
            field=models.CharField(default='purchase', max_length=20),
        ),
    ]

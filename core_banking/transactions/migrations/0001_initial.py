# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-24 21:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_auto_20170924_2120'),
    ]

    operations = [
        migrations.CreateModel(
            name='Journals',
            fields=[
                ('transaction_id', models.IntegerField(primary_key=True, serialize=False)),
                ('transaction_type', models.CharField(max_length=20)),
                ('timestamp', models.DateTimeField(verbose_name='date of transaction')),
                ('purchase_amount', models.FloatField(default=0)),
                ('amount_to_date', models.IntegerField(default=0)),
                ('account_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Accounts')),
            ],
        ),
    ]

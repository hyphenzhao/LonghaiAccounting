# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-15 06:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0016_auto_20180214_0950'),
    ]

    operations = [
        migrations.AddField(
            model_name='income',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]

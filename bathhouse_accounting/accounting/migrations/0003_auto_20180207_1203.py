# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-07 12:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_income_card_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systemuser',
            name='phone',
            field=models.CharField(max_length=30, null=True),
        ),
    ]

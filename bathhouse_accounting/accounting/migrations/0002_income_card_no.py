# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-07 09:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='income',
            name='card_no',
            field=models.CharField(default=0, max_length=60),
            preserve_default=False,
        ),
    ]

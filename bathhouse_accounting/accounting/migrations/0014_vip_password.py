# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-14 01:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0013_auto_20180212_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='vip',
            name='password',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]

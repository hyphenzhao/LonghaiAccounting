# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-12 07:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0012_auto_20180212_1036'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service',
            old_name='income_id',
            new_name='income',
        ),
        migrations.RenameField(
            model_name='service',
            old_name='item_id',
            new_name='item',
        ),
        migrations.RenameField(
            model_name='service',
            old_name='staff_id',
            new_name='staff',
        ),
    ]

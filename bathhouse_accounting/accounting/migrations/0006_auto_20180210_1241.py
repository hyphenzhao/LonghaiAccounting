# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-10 04:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0005_paymentmethod_if_deleted'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paymentmethod',
            old_name='if_deleted',
            new_name='is_deleted',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-15 13:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0019_auto_20180215_1809'),
    ]

    operations = [
        migrations.CreateModel(
            name='VIPPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounting.PaymentMethod')),
            ],
        ),
    ]

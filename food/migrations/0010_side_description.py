# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-23 01:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0009_auto_20170213_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='side',
            name='description',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-13 11:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0005_auto_20170213_1113'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Sides',
            new_name='Side',
        ),
    ]
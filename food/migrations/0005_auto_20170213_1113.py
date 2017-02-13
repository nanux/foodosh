# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-13 11:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0004_mealplan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sides',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('value', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='mealplan',
            name='childCount',
            field=models.IntegerField(default=130),
        ),
    ]

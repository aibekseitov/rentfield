# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-09 11:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Field', '0009_auto_20170409_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
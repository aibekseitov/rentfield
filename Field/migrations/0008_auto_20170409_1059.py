# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-09 10:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Field', '0007_auto_20170409_0434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
    ]

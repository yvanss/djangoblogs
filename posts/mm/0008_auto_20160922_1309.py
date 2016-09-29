# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-22 10:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20160921_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='publish',
            field=models.DateField(auto_now=True, default=datetime.datetime(2016, 9, 22, 10, 9, 5, 515000, tzinfo=utc)),
            preserve_default=False,
        ),
    ]

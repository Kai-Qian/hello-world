# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0006_auto_20160214_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='posting',
            name='time',
            field=models.IntegerField(default=datetime.datetime.now),
        ),
    ]

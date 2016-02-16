# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0009_auto_20160215_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posting',
            name='time',
            field=models.IntegerField(default=1455561885.923),
        ),
    ]

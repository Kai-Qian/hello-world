# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0011_remove_posting_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='posting',
            name='time',
            field=models.IntegerField(default=1455561990.95),
        ),
    ]

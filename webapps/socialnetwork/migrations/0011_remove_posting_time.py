# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0010_auto_20160215_1344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posting',
            name='time',
        ),
    ]

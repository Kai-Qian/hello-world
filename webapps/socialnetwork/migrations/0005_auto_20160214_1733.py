# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0004_followers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followers',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]

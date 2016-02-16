# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('socialnetwork', '0005_auto_20160214_1733'),
    ]

    operations = [
        migrations.CreateModel(
            name='Followings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('countForFollowings', models.IntegerField(default=0)),
                ('followings', models.ManyToManyField(related_name='followings', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='user', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='followers',
            name='followers',
        ),
        migrations.RemoveField(
            model_name='followers',
            name='user',
        ),
        migrations.DeleteModel(
            name='Followers',
        ),
    ]

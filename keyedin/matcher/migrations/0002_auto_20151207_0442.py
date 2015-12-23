# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matcher', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='boxes',
            field=models.ManyToManyField(related_name='tracks', to='matcher.Box', blank=True),
        ),
    ]

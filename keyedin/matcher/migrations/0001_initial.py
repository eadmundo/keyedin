# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Key',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('name', models.CharField(max_length=1, choices=[(b'C', b'C'), (b'C#', b'C#'), (b'D', b'D'), (b'D#', b'D#'), (b'E', b'E'), (b'F', b'F'), (b'F#', b'F#'), (b'G', b'G'), (b'G#', b'G#'), (b'A', b'A'), (b'A#', b'A#'), (b'B', b'B')])),
                ('minor', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('artist', models.CharField(max_length=255)),
                ('bpm', models.FloatField()),
                ('boxes', models.ManyToManyField(related_name='tracks', to='matcher.Box')),
                ('key', models.ForeignKey(to='matcher.Key')),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-24 04:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('route', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggest',
            name='lat',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='suggest',
            name='lng',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-25 08:22
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('route', '0006_suggest_google_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggest',
            name='google_images',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(), default=[], size=None),
            preserve_default=False,
        ),
    ]
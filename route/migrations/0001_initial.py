# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-24 04:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Suggest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('lat', models.DecimalField(decimal_places=3, max_digits=5)),
                ('lng', models.DecimalField(decimal_places=3, max_digits=5)),
                ('place_id', models.CharField(max_length=255, unique=True)),
                ('province', models.CharField(max_length=80)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

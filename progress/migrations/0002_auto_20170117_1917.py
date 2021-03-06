# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-17 19:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('progress', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='progress',
            options={'verbose_name_plural': 'Progresses'},
        ),
        migrations.AddField(
            model_name='progress',
            name='code_name',
            field=models.SlugField(default=''),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='percentage',
            field=models.IntegerField(default=0, help_text='0 mean auto calculate'),
        ),
        migrations.AlterField(
            model_name='progress',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='belong', to='progress.Milestone'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-30 12:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20160427_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='category',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='project',
            name='descrip',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(max_length=110),
        ),
    ]

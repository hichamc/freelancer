# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-24 19:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20160424_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_shortname',
            field=models.CharField(max_length=20),
        ),
    ]
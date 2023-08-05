# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-18 13:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0005_customer_domain'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='backend_id',
            field=models.CharField(blank=True, help_text='Organization identifier in another application.', max_length=255),
        ),
    ]

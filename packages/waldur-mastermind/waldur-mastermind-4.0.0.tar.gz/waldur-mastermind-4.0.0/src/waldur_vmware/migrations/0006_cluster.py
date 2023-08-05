# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-06-28 12:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import waldur_core.core.fields
import waldur_core.core.models
import waldur_core.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0009_project_is_removed'),
        ('waldur_vmware', '0005_virtualmachine_template'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, validators=[waldur_core.core.validators.validate_name], verbose_name='name')),
                ('uuid', waldur_core.core.fields.UUIDField()),
                ('backend_id', models.CharField(db_index=True, max_length=255)),
                ('settings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='structure.ServiceSettings')),
            ],
            options={
                'abstract': False,
            },
            bases=(waldur_core.core.models.BackendModelMixin, models.Model),
        ),
        migrations.AddField(
            model_name='virtualmachine',
            name='cluster',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='waldur_vmware.Cluster'),
        ),
        migrations.AlterUniqueTogether(
            name='cluster',
            unique_together=set([('settings', 'backend_id')]),
        ),
    ]

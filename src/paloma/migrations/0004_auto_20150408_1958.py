# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paloma', '0003_auto_20150309_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publish',
            name='status',
            field=models.CharField(default=b'pending', choices=[(b'pending', 'Pending'), (b'scheduled', 'Scheduled'), (b'active', 'Active'), (b'finished', 'Finished'), (b'canceled', 'Canceled')], max_length=24, help_text='Publish Status Help', verbose_name='Publish Status', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publish',
            name='text',
            field=models.TextField(verbose_name='Text'),
            preserve_default=True,
        ),
    ]

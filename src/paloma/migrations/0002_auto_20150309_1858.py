# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paloma', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alias',
            options={'verbose_name': 'Alias', 'verbose_name_plural': 'Alias'},
        ),
        migrations.AlterField(
            model_name='alias',
            name='address',
            field=models.CharField(max_length=100, verbose_name='Alias Address'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='alias',
            name='alias',
            field=models.CharField(default='hoge', max_length=100, verbose_name='Alias Forward'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='alias',
            unique_together=set([('address', 'alias')]),
        ),
    ]

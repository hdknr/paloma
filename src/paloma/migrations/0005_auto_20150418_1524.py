# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paloma', '0004_auto_20150408_1958'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='site',
            options={'verbose_name': 'Site', 'verbose_name_plural': 'Site'},
        ),
        migrations.AlterUniqueTogether(
            name='site',
            unique_together=set([('name', 'domain')]),
        ),
    ]

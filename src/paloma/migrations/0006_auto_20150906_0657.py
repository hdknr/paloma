# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('paloma', '0005_auto_20150418_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='circle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='paloma.Circle', null=True, verbose_name='Circle'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='domain',
            field=models.CharField(default=b'localhost', max_length=100, help_text='@Domain', unique=True, verbose_name='@Domain', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='name',
            field=models.CharField(help_text='Owner Site Name', unique=True, max_length=100, verbose_name='Owner Site Name', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='operators',
            field=models.ManyToManyField(help_text='User', to=settings.AUTH_USER_MODEL, verbose_name='Site Operators'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='url',
            field=models.CharField(default=b'/', max_length=150, help_text='URL', unique=True, verbose_name='URL', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='template',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Template Name', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='template',
            name='text',
            field=models.TextField(default=b'', verbose_name='Template Text'),
            preserve_default=True,
        ),
    ]

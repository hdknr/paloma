# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(unique=True, max_length=100)),
                ('alias', models.CharField(default=None, max_length=100, null=True, blank=True)),
                ('mailbox', models.CharField(default=None, max_length=100, blank=True, help_text='specify Maildir path if address is local user ', null=True, verbose_name='Mailbox')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Circle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Circle Name', db_index=True)),
                ('description', models.TextField(default=None, null=True, verbose_name='Circle Description', blank=True)),
                ('symbol', models.CharField(help_text='Circle Symbol Help Text', max_length=100, verbose_name='Circle Symbol', db_index=True)),
                ('is_default', models.BooleanField(default=False, help_text='Is Default Circle Help', verbose_name='Is Default Circle')),
                ('is_moderated', models.BooleanField(default=True, help_text='Is Moderated Circle Help', verbose_name='Is Moderated Circle')),
                ('is_secret', models.BooleanField(default=False, help_text='Is Secret Circle Help', verbose_name='Is Secret Circle')),
            ],
            options={
                'verbose_name': 'Circle',
                'verbose_name_plural': 'Circles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain', models.CharField(unique=True, max_length=100, verbose_name='Domain', db_index=True)),
                ('description', models.CharField(default=b'', max_length=200, verbose_name='Description')),
                ('maxquota', models.BigIntegerField(default=None, null=True, blank=True)),
                ('quota', models.BigIntegerField(default=None, null=True, blank=True)),
                ('transport', models.CharField(max_length=765)),
                ('backupmx', models.IntegerField(default=None, null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Domain',
                'verbose_name_plural': 'Domains',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dt_created', models.DateTimeField(help_text='Journaled datetime', verbose_name='Journaled Datetime', auto_now_add=True)),
                ('sender', models.CharField(max_length=100, verbose_name='Sender')),
                ('recipient', models.CharField(max_length=100, verbose_name='Receipient')),
                ('text', models.TextField(default=None, null=True, verbose_name='Message Text', blank=True)),
                ('is_jailed', models.BooleanField(default=False, verbose_name='Jailed Message')),
            ],
            options={
                'verbose_name': 'Journal',
                'verbose_name_plural': 'Journals',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(unique=True, max_length=100, verbose_name='Forward address')),
                ('is_active', models.BooleanField(default=False, verbose_name='Actaive status')),
                ('bounces', models.IntegerField(default=0, verbose_name='Bounce counts')),
            ],
            options={
                'verbose_name': 'Member',
                'verbose_name_plural': 'Members',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_admin', models.BooleanField(default=False, verbose_name='Is Circle Admin')),
                ('is_admitted', models.BooleanField(default=False, help_text='Is Membership Admitted Help', verbose_name='Is Membership Admitted')),
                ('circle', models.ForeignKey(verbose_name='Circle', to='paloma.Circle')),
                ('member', models.ForeignKey(verbose_name='Member', to='paloma.Member')),
            ],
            options={
                'verbose_name': 'Membership',
                'verbose_name_plural': 'Memberships',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mail_message_id', models.CharField(unique=True, max_length=100, verbose_name='Message ID', db_index=True)),
                ('recipient', models.EmailField(default=None, max_length=50, null=True, verbose_name='recipient', blank=True)),
                ('subject', models.TextField(default=None, null=True, verbose_name='Message Subject', blank=True)),
                ('text', models.TextField(default=None, null=True, verbose_name='Message Text', blank=True)),
                ('status', models.CharField(default=None, max_length=50, null=True, verbose_name='Status', blank=True)),
                ('task_id', models.CharField(default=None, max_length=40, null=True, verbose_name='Task ID', blank=True)),
                ('checked', models.BooleanField(default=False, verbose_name='Mail Checked')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('smtped', models.DateTimeField(default=None, null=True, verbose_name='SMTP Time', blank=True)),
                ('parameters', models.TextField(null=True, blank=True)),
                ('circle', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, verbose_name='Circle', to='paloma.Circle', null=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='paloma.Member', null=True, verbose_name='Member')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Provision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=24, verbose_name='Provision Status', db_index=True)),
                ('prospect', models.CharField(default=None, max_length=100, null=True, verbose_name='Provision Prospect', blank=True)),
                ('secret', models.CharField(default=b'', unique=True, max_length=100, verbose_name='Provision Secret')),
                ('short_secret', models.CharField(default=b'', unique=True, max_length=10, verbose_name='Provision Short Secret')),
                ('url', models.CharField(default=None, max_length=200, null=True, verbose_name='URL for Notice', blank=True)),
                ('dt_expire', models.DateTimeField(default=None, help_text='Secrete Expired', null=True, verbose_name='Provision Secret Expired', blank=True)),
                ('dt_try', models.DateTimeField(default=None, help_text='Try Datetime', null=True, verbose_name='Provision Try Datetime', blank=True)),
                ('dt_commit', models.DateTimeField(default=None, help_text='Commit Datetime', null=True, verbose_name='Commit Datetime', blank=True)),
                ('circle', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='paloma.Circle', null=True, verbose_name='Circle')),
                ('inviter', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='Inviter')),
                ('member', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, default=None, to='paloma.Member', blank=True, verbose_name='Member')),
            ],
            options={
                'verbose_name': 'Provision',
                'verbose_name_plural': 'Provisions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.ForeignKey(verbose_name='Mail Message', to='paloma.Message')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Publish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=101, verbose_name='Subject')),
                ('text', models.TextField(max_length=100, verbose_name='Text')),
                ('task_id', models.CharField(default=None, max_length=40, null=True, verbose_name='Task ID', blank=True)),
                ('status', models.CharField(default=b'pending', choices=[(b'pending', b'pending'), (b'scheduled', b'scheduled'), (b'active', b'active'), (b'finished', b'finished'), (b'canceled', b'canceled')], max_length=24, help_text='Publish Status Help', verbose_name='Publish Status', db_index=True)),
                ('dt_start', models.DateTimeField(default=django.utils.timezone.now, help_text='Time to Send Help', null=True, verbose_name='Time to Send', blank=True)),
                ('activated_at', models.DateTimeField(default=None, help_text='Task Activated Time Help', null=True, verbose_name='Task Activated Time', blank=True)),
                ('forward_to', models.CharField(default=None, max_length=100, null=True, verbose_name='Forward address', blank=True)),
                ('circles', models.ManyToManyField(to='paloma.Circle', verbose_name='Target Circles')),
                ('messages', models.ManyToManyField(related_name='message_set', verbose_name='Messages', through='paloma.Publication', to='paloma.Message')),
                ('publisher', models.ForeignKey(verbose_name='Publisher', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Publish',
                'verbose_name_plural': 'Publish',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='Owner Site Name', db_index=True)),
                ('domain', models.CharField(default=b'localhost', unique=True, max_length=100, verbose_name='@Domain', db_index=True)),
                ('url', models.CharField(default=b'/', unique=True, max_length=150, verbose_name='URL', db_index=True)),
                ('operators', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Site Operators')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Systemevent',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('customerid', models.BigIntegerField(null=True, db_column='CustomerID', blank=True)),
                ('receivedat', models.DateTimeField(null=True, db_column='ReceivedAt', blank=True)),
                ('devicereportedtime', models.DateTimeField(null=True, db_column='DeviceReportedTime', blank=True)),
                ('facility', models.IntegerField(null=True, db_column='Facility', blank=True)),
                ('priority', models.IntegerField(null=True, db_column='Priority', blank=True)),
                ('fromhost', models.CharField(max_length=60L, db_column='FromHost', blank=True)),
                ('message', models.TextField(db_column='Message', blank=True)),
                ('ntseverity', models.IntegerField(null=True, db_column='NTSeverity', blank=True)),
                ('importance', models.IntegerField(null=True, db_column='Importance', blank=True)),
                ('eventsource', models.CharField(max_length=60L, db_column='EventSource', blank=True)),
                ('eventuser', models.CharField(max_length=60L, db_column='EventUser', blank=True)),
                ('eventcategory', models.IntegerField(null=True, db_column='EventCategory', blank=True)),
                ('eventid', models.IntegerField(null=True, db_column='EventID', blank=True)),
                ('eventbinarydata', models.TextField(db_column='EventBinaryData', blank=True)),
                ('maxavailable', models.IntegerField(null=True, db_column='MaxAvailable', blank=True)),
                ('currusage', models.IntegerField(null=True, db_column='CurrUsage', blank=True)),
                ('minusage', models.IntegerField(null=True, db_column='MinUsage', blank=True)),
                ('maxusage', models.IntegerField(null=True, db_column='MaxUsage', blank=True)),
                ('infounitid', models.IntegerField(null=True, db_column='InfoUnitID', blank=True)),
                ('syslogtag', models.CharField(max_length=60L, db_column='SysLogTag', blank=True)),
                ('eventlogtype', models.CharField(max_length=60L, db_column='EventLogType', blank=True)),
                ('genericfilename', models.CharField(max_length=60L, db_column='GenericFileName', blank=True)),
                ('systemid', models.IntegerField(null=True, db_column='SystemID', blank=True)),
            ],
            options={
                'db_table': 'SystemEvents',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Systemeventsproperty',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('systemeventid', models.IntegerField(null=True, db_column='SystemEventID', blank=True)),
                ('paramname', models.CharField(max_length=255L, db_column='ParamName', blank=True)),
                ('paramvalue', models.TextField(db_column='ParamValue', blank=True)),
            ],
            options={
                'db_table': 'SystemEventsProperties',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Targetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('targetter_object_id', models.PositiveIntegerField()),
                ('mediator_object_id', models.PositiveIntegerField()),
                ('mediator_content_type', models.ForeignKey(related_name='mediator', to='contenttypes.ContentType')),
                ('site', models.ForeignKey(verbose_name='Owner Site', to='paloma.Site')),
                ('targetter_content_type', models.ForeignKey(related_name='targetter', to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Template Name', db_index=True)),
                ('subject', models.CharField(default=b'', max_length=100, verbose_name='Template Subject')),
                ('text', models.TextField(default=b'', max_length=100, verbose_name='Template Text')),
                ('site', models.ForeignKey(verbose_name='Owner Site', to='paloma.Site')),
            ],
            options={
                'verbose_name': 'Template',
                'verbose_name_plural': 'Templates',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='template',
            unique_together=set([('site', 'name')]),
        ),
        migrations.AddField(
            model_name='publish',
            name='site',
            field=models.ForeignKey(verbose_name='Site', to='paloma.Site'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='publication',
            name='publish',
            field=models.ForeignKey(verbose_name='Publish', to='paloma.Publish'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Template', to='paloma.Template', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together=set([('member', 'circle')]),
        ),
        migrations.AddField(
            model_name='member',
            name='circles',
            field=models.ManyToManyField(to='paloma.Circle', verbose_name='Opt-in Circle', through='paloma.Membership'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='user',
            field=models.ForeignKey(verbose_name='System User', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='circle',
            name='site',
            field=models.ForeignKey(verbose_name='Owner Site', to='paloma.Site'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='circle',
            unique_together=set([('site', 'symbol'), ('site', 'name')]),
        ),
    ]

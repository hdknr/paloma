# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Domain'
        db.create_table(u'paloma_domain', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('domain', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, db_index=True)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('maxquota', self.gf('django.db.models.fields.BigIntegerField')(default=None, null=True, blank=True)),
            ('quota', self.gf('django.db.models.fields.BigIntegerField')(default=None, null=True, blank=True)),
            ('transport', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('backupmx', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'paloma', ['Domain'])

        # Adding model 'Alias'
        db.create_table(u'paloma_alias', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('alias', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True)),
            ('mailbox', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'paloma', ['Alias'])

        # Adding model 'Owner'
        db.create_table(u'paloma_owner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, db_index=True)),
            ('domain', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, db_index=True)),
            ('forward_to', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'paloma', ['Owner'])

        # Adding model 'Operator'
        db.create_table(u'paloma_operator', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['paloma.Owner'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'paloma', ['Operator'])

        # Adding model 'Group'
        db.create_table(u'paloma_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['paloma.Owner'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
        ))
        db.send_create_signal(u'paloma', ['Group'])

        # Adding unique constraint on 'Group', fields ['owner', 'name']
        db.create_unique(u'paloma_group', ['owner_id', 'name'])

        # Adding unique constraint on 'Group', fields ['owner', 'symbol']
        db.create_unique(u'paloma_group', ['owner_id', 'symbol'])

        # Adding model 'Mailbox'
        db.create_table(u'paloma_mailbox', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('address', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('bounces', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'paloma', ['Mailbox'])

        # Adding M2M table for field groups on 'Mailbox'
        db.create_table(u'paloma_mailbox_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mailbox', models.ForeignKey(orm[u'paloma.mailbox'], null=False)),
            ('group', models.ForeignKey(orm[u'paloma.group'], null=False))
        ))
        db.create_unique(u'paloma_mailbox_groups', ['mailbox_id', 'group_id'])

        # Adding model 'Enroll'
        db.create_table(u'paloma_enroll', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mailbox', self.gf('django.db.models.fields.related.OneToOneField')(null=True, on_delete=models.SET_NULL, default=None, to=orm['paloma.Mailbox'], blank=True, unique=True)),
            ('enroll_type', self.gf('django.db.models.fields.CharField')(default='activate', max_length=24, db_index=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['paloma.Group'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('inviter', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['auth.User'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('prospect', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True)),
            ('secret', self.gf('django.db.models.fields.CharField')(default='SKQDvUeSroqBkEsBAVUvZC1RjMrm7gfN', unique=True, max_length=100)),
            ('short_secret', self.gf('django.db.models.fields.CharField')(default='0aoRxy72', unique=True, max_length=10)),
            ('url', self.gf('django.db.models.fields.CharField')(default=None, max_length=200, null=True, blank=True)),
            ('dt_expire', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('dt_try', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('dt_commit', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal(u'paloma', ['Enroll'])

        # Adding model 'Notice'
        db.create_table(u'paloma_notice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['paloma.Owner'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=100)),
        ))
        db.send_create_signal(u'paloma', ['Notice'])

        # Adding model 'Schedule'
        db.create_table(u'paloma_schedule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['paloma.Owner'])),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=101)),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=100)),
            ('task', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='pending', max_length=24, db_index=True)),
            ('dt_start', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('forward_to', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'paloma', ['Schedule'])

        # Adding M2M table for field groups on 'Schedule'
        db.create_table(u'paloma_schedule_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('schedule', models.ForeignKey(orm[u'paloma.schedule'], null=False)),
            ('group', models.ForeignKey(orm[u'paloma.group'], null=False))
        ))
        db.create_unique(u'paloma_schedule_groups', ['schedule_id', 'group_id'])

        # Adding model 'Message'
        db.create_table(u'paloma_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['paloma.Schedule'])),
            ('mailbox', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['paloma.Mailbox'])),
            ('mail_message_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, db_index=True)),
            ('text', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal(u'paloma', ['Message'])

        # Adding model 'Journal'
        db.create_table(u'paloma_journal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dt_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('sender', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('recipient', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('text', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
            ('is_jailed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'paloma', ['Journal'])

        # Adding model 'EmailTask'
        db.create_table(u'paloma_emailtask', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200, db_index=True)),
            ('task_module', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('task_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('task_key', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('dt_expire', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal(u'paloma', ['EmailTask'])

        # Adding model 'Site'
        db.create_table(u'paloma_site', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, db_index=True)),
            ('domain', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, db_index=True)),
        ))
        db.send_create_signal(u'paloma', ['Site'])

        # Adding M2M table for field operators on 'Site'
        db.create_table(u'paloma_site_operators', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('site', models.ForeignKey(orm[u'paloma.site'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(u'paloma_site_operators', ['site_id', 'user_id'])

        # Adding model 'Circle'
        db.create_table(u'paloma_circle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['paloma.Site'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('is_default', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'paloma', ['Circle'])

        # Adding unique constraint on 'Circle', fields ['site', 'name']
        db.create_unique(u'paloma_circle', ['site_id', 'name'])

        # Adding unique constraint on 'Circle', fields ['site', 'symbol']
        db.create_unique(u'paloma_circle', ['site_id', 'symbol'])


    def backwards(self, orm):
        # Removing unique constraint on 'Circle', fields ['site', 'symbol']
        db.delete_unique(u'paloma_circle', ['site_id', 'symbol'])

        # Removing unique constraint on 'Circle', fields ['site', 'name']
        db.delete_unique(u'paloma_circle', ['site_id', 'name'])

        # Removing unique constraint on 'Group', fields ['owner', 'symbol']
        db.delete_unique(u'paloma_group', ['owner_id', 'symbol'])

        # Removing unique constraint on 'Group', fields ['owner', 'name']
        db.delete_unique(u'paloma_group', ['owner_id', 'name'])

        # Deleting model 'Domain'
        db.delete_table(u'paloma_domain')

        # Deleting model 'Alias'
        db.delete_table(u'paloma_alias')

        # Deleting model 'Owner'
        db.delete_table(u'paloma_owner')

        # Deleting model 'Operator'
        db.delete_table(u'paloma_operator')

        # Deleting model 'Group'
        db.delete_table(u'paloma_group')

        # Deleting model 'Mailbox'
        db.delete_table(u'paloma_mailbox')

        # Removing M2M table for field groups on 'Mailbox'
        db.delete_table('paloma_mailbox_groups')

        # Deleting model 'Enroll'
        db.delete_table(u'paloma_enroll')

        # Deleting model 'Notice'
        db.delete_table(u'paloma_notice')

        # Deleting model 'Schedule'
        db.delete_table(u'paloma_schedule')

        # Removing M2M table for field groups on 'Schedule'
        db.delete_table('paloma_schedule_groups')

        # Deleting model 'Message'
        db.delete_table(u'paloma_message')

        # Deleting model 'Journal'
        db.delete_table(u'paloma_journal')

        # Deleting model 'EmailTask'
        db.delete_table(u'paloma_emailtask')

        # Deleting model 'Site'
        db.delete_table(u'paloma_site')

        # Removing M2M table for field operators on 'Site'
        db.delete_table('paloma_site_operators')

        # Deleting model 'Circle'
        db.delete_table(u'paloma_circle')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'paloma.alias': {
            'Meta': {'object_name': 'Alias'},
            'address': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'alias': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailbox': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'paloma.circle': {
            'Meta': {'unique_together': "(('site', 'name'), ('site', 'symbol'))", 'object_name': 'Circle'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['paloma.Site']"}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        u'paloma.domain': {
            'Meta': {'object_name': 'Domain'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'backupmx': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'domain': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maxquota': ('django.db.models.fields.BigIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'quota': ('django.db.models.fields.BigIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'transport': ('django.db.models.fields.CharField', [], {'max_length': '765'})
        },
        u'paloma.emailtask': {
            'Meta': {'object_name': 'EmailTask'},
            'dt_expire': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'task_key': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'task_module': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'task_name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'paloma.enroll': {
            'Meta': {'object_name': 'Enroll'},
            'dt_commit': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'dt_expire': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'dt_try': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'enroll_type': ('django.db.models.fields.CharField', [], {'default': "'activate'", 'max_length': '24', 'db_index': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['paloma.Group']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inviter': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'mailbox': ('django.db.models.fields.related.OneToOneField', [], {'null': 'True', 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': u"orm['paloma.Mailbox']", 'blank': 'True', 'unique': 'True'}),
            'prospect': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'default': "'BN2L40ysD7tijV8R8jGaJKJnYJO4FDSl'", 'unique': 'True', 'max_length': '100'}),
            'short_secret': ('django.db.models.fields.CharField', [], {'default': "'FnoOJ9i6'", 'unique': 'True', 'max_length': '10'}),
            'url': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'paloma.group': {
            'Meta': {'unique_together': "(('owner', 'name'), ('owner', 'symbol'))", 'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['paloma.Owner']"}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        u'paloma.journal': {
            'Meta': {'object_name': 'Journal'},
            'dt_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_jailed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recipient': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'text': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        u'paloma.mailbox': {
            'Meta': {'object_name': 'Mailbox'},
            'address': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'bounces': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['paloma.Group']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'paloma.message': {
            'Meta': {'object_name': 'Message'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail_message_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'mailbox': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['paloma.Mailbox']"}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['paloma.Schedule']"}),
            'text': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        u'paloma.notice': {
            'Meta': {'object_name': 'Notice'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['paloma.Owner']"}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '100'})
        },
        u'paloma.operator': {
            'Meta': {'object_name': 'Operator'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['paloma.Owner']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'paloma.owner': {
            'Meta': {'object_name': 'Owner'},
            'domain': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'forward_to': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'paloma.schedule': {
            'Meta': {'object_name': 'Schedule'},
            'dt_start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'forward_to': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['paloma.Group']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['paloma.Owner']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '24', 'db_index': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '101'}),
            'task': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '100'})
        },
        u'paloma.site': {
            'Meta': {'object_name': 'Site'},
            'domain': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'operators': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['paloma']
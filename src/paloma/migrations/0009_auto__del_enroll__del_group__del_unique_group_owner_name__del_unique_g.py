# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Group', fields ['owner', 'symbol']
        db.delete_unique(u'paloma_group', ['owner_id', 'symbol'])

        # Removing unique constraint on 'Group', fields ['owner', 'name']
        db.delete_unique(u'paloma_group', ['owner_id', 'name'])

        # Deleting model 'Enroll'
        db.delete_table(u'paloma_enroll')

        # Deleting model 'Group'
        db.delete_table(u'paloma_group')

        # Deleting model 'Operator'
        db.delete_table(u'paloma_operator')

        # Deleting model 'Owner'
        db.delete_table(u'paloma_owner')

        # Deleting model 'Notice'
        db.delete_table(u'paloma_notice')

        # Deleting model 'Message'
        db.delete_table(u'paloma_message')

        # Deleting model 'EmailTask'
        db.delete_table(u'paloma_emailtask')

        # Deleting model 'Schedule'
        db.delete_table(u'paloma_schedule')

        # Removing M2M table for field groups on 'Schedule'
        db.delete_table('paloma_schedule_groups')

        # Deleting model 'Mailbox'
        db.delete_table(u'paloma_mailbox')

        # Removing M2M table for field groups on 'Mailbox'
        db.delete_table('paloma_mailbox_groups')


    def backwards(self, orm):
        # Adding model 'Enroll'
        db.create_table(u'paloma_enroll', (
            ('prospect', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True)),
            ('mailbox', self.gf('django.db.models.fields.related.OneToOneField')(null=True, on_delete=models.SET_NULL, default=None, to=orm['paloma.Mailbox'], blank=True, unique=True)),
            ('dt_try', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['paloma.Group'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(default=None, max_length=200, null=True, blank=True)),
            ('short_secret', self.gf('django.db.models.fields.CharField')(default='TTycJhRM', max_length=10, unique=True)),
            ('dt_commit', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('enroll_type', self.gf('django.db.models.fields.CharField')(default='activate', max_length=24, db_index=True)),
            ('secret', self.gf('django.db.models.fields.CharField')(default='HvaycK6pmlUV7JwpzOCuMBQR3YFenl1D', max_length=100, unique=True)),
            ('inviter', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['auth.User'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('dt_expire', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal(u'paloma', ['Enroll'])

        # Adding model 'Group'
        db.create_table(u'paloma_group', (
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['paloma.Owner'])),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
        ))
        db.send_create_signal(u'paloma', ['Group'])

        # Adding unique constraint on 'Group', fields ['owner', 'name']
        db.create_unique(u'paloma_group', ['owner_id', 'name'])

        # Adding unique constraint on 'Group', fields ['owner', 'symbol']
        db.create_unique(u'paloma_group', ['owner_id', 'symbol'])

        # Adding model 'Operator'
        db.create_table(u'paloma_operator', (
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['paloma.Owner'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'paloma', ['Operator'])

        # Adding model 'Owner'
        db.create_table(u'paloma_owner', (
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True, db_index=True)),
            ('forward_to', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'paloma', ['Owner'])

        # Adding model 'Notice'
        db.create_table(u'paloma_notice', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=100)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['paloma.Owner'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'paloma', ['Notice'])

        # Adding model 'Message'
        db.create_table(u'paloma_message', (
            ('mail_message_id', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True, db_index=True)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['paloma.Schedule'])),
            ('text', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
            ('mailbox', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['paloma.Mailbox'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'paloma', ['Message'])

        # Adding model 'EmailTask'
        db.create_table(u'paloma_emailtask', (
            ('task_module', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=200, unique=True, db_index=True)),
            ('task_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('dt_expire', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task_key', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'paloma', ['EmailTask'])

        # Adding model 'Schedule'
        db.create_table(u'paloma_schedule', (
            ('status', self.gf('django.db.models.fields.CharField')(default='pending', max_length=24, db_index=True)),
            ('task', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['paloma.Owner'])),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=100)),
            ('forward_to', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=101)),
            ('dt_start', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'paloma', ['Schedule'])

        # Adding M2M table for field groups on 'Schedule'
        db.create_table(u'paloma_schedule_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('schedule', models.ForeignKey(orm[u'paloma.schedule'], null=False)),
            ('group', models.ForeignKey(orm[u'paloma.group'], null=False))
        ))
        db.create_unique(u'paloma_schedule_groups', ['schedule_id', 'group_id'])

        # Adding model 'Mailbox'
        db.create_table(u'paloma_mailbox', (
            ('bounces', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'paloma', ['Mailbox'])

        # Adding M2M table for field groups on 'Mailbox'
        db.create_table(u'paloma_mailbox_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mailbox', models.ForeignKey(orm[u'paloma.mailbox'], null=False)),
            ('group', models.ForeignKey(orm[u'paloma.group'], null=False))
        ))
        db.create_unique(u'paloma_mailbox_groups', ['mailbox_id', 'group_id'])


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
            'operators': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
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
        u'paloma.journal': {
            'Meta': {'object_name': 'Journal'},
            'dt_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_jailed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recipient': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'text': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        u'paloma.mail': {
            'Meta': {'object_name': 'Mail'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail_message_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['paloma.Member']"}),
            'publish': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['paloma.Publish']"}),
            'text': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        u'paloma.member': {
            'Meta': {'object_name': 'Member'},
            'address': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'bounces': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'circles': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['paloma.Circle']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'paloma.provision': {
            'Meta': {'object_name': 'Provision'},
            'circle': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['paloma.Circle']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'dt_commit': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'dt_expire': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 4, 4, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'dt_try': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inviter': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'member': ('django.db.models.fields.related.OneToOneField', [], {'null': 'True', 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': u"orm['paloma.Member']", 'blank': 'True', 'unique': 'True'}),
            'prospect': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'default': "'OJYdpQhruY5a0KE1dHiscn5lmYbCpDPQ'", 'unique': 'True', 'max_length': '100'}),
            'short_secret': ('django.db.models.fields.CharField', [], {'default': "'CK8zYGJa'", 'unique': 'True', 'max_length': '10'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '24', 'db_index': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'paloma.publish': {
            'Meta': {'object_name': 'Publish'},
            'circles': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['paloma.Circle']", 'symmetrical': 'False'}),
            'dt_start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'forward_to': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['paloma.Site']"}),
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
            'operators': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150', 'db_index': 'True'})
        },
        u'paloma.text': {
            'Meta': {'unique_together': "(('site', 'name'),)", 'object_name': 'Text'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['paloma.Site']"}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['paloma']
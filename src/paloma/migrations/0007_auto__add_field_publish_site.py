# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Publish.site'
        db.add_column(u'paloma_publish', 'site',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['paloma.Site'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Publish.site'
        db.delete_column(u'paloma_publish', 'site_id')


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
            'secret': ('django.db.models.fields.CharField', [], {'default': "'g33RXS958xrfJeGGMhH8WmSnofH2QVdp'", 'unique': 'True', 'max_length': '100'}),
            'short_secret': ('django.db.models.fields.CharField', [], {'default': "'qBQewRik'", 'unique': 'True', 'max_length': '10'}),
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
        u'paloma.mail': {
            'Meta': {'object_name': 'Mail'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail_message_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['paloma.Member']"}),
            'publish': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['paloma.Publish']"}),
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
        u'paloma.member': {
            'Meta': {'object_name': 'Member'},
            'address': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'bounces': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'circles': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['paloma.Circle']", 'symmetrical': 'False'}),
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
            'secret': ('django.db.models.fields.CharField', [], {'default': "'eTMVTS6eoabpRm99c2zBByTpsXhcTKq5'", 'unique': 'True', 'max_length': '100'}),
            'short_secret': ('django.db.models.fields.CharField', [], {'default': "'AnvusK1y'", 'unique': 'True', 'max_length': '10'}),
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
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['paloma.Site']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '24', 'db_index': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '101'}),
            'task': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '100'})
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
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Publish.dt_start'
        db.alter_column(u'paloma_publish', 'dt_start', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):

        # Changing field 'Publish.dt_start'
        db.alter_column(u'paloma_publish', 'dt_start', self.gf('django.db.models.fields.DateTimeField')())

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
            'is_moderated': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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
        u'paloma.journal': {
            'Meta': {'object_name': 'Journal'},
            'dt_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_jailed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recipient': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'text': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        u'paloma.member': {
            'Meta': {'object_name': 'Member'},
            'address': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'bounces': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'circles': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['paloma.Circle']", 'through': u"orm['paloma.Membership']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'paloma.membership': {
            'Meta': {'object_name': 'Membership'},
            'circle': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['paloma.Circle']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['paloma.Member']"})
        },
        u'paloma.message': {
            'Meta': {'object_name': 'Message'},
            'circle': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['paloma.Circle']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail_message_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['paloma.Member']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'parameters': ('json_field.fields.JSONField', [], {'default': "'null'", 'null': 'True', 'blank': 'True'}),
            'recipient': ('django.db.models.fields.EmailField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'smtped': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'task_id': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['paloma.Template']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'text': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'paloma.provision': {
            'Meta': {'object_name': 'Provision'},
            'circle': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['paloma.Circle']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'dt_commit': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'dt_expire': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'dt_try': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inviter': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'member': ('django.db.models.fields.related.OneToOneField', [], {'null': 'True', 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': u"orm['paloma.Member']", 'blank': 'True', 'unique': 'True'}),
            'prospect': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'default': "'jgRZjNLlnx31fsMU4gPHLL0YsHTq2is8'", 'unique': 'True', 'max_length': '100'}),
            'short_secret': ('django.db.models.fields.CharField', [], {'default': "'4t9LRoqe'", 'unique': 'True', 'max_length': '10'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '24', 'db_index': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'paloma.publication': {
            'Meta': {'object_name': 'Publication'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['paloma.Message']"}),
            'publish': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['paloma.Publish']"})
        },
        u'paloma.publish': {
            'Meta': {'object_name': 'Publish'},
            'circles': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['paloma.Circle']", 'symmetrical': 'False'}),
            'dt_start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'forward_to': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'message_set'", 'symmetrical': 'False', 'through': u"orm['paloma.Publication']", 'to': u"orm['paloma.Message']"}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['paloma.Site']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '24', 'db_index': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '101'}),
            'task_id': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '100'})
        },
        u'paloma.site': {
            'Meta': {'object_name': 'Site'},
            'domain': ('django.db.models.fields.CharField', [], {'default': "'localhost'", 'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'operators': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.CharField', [], {'default': "'/'", 'unique': 'True', 'max_length': '150', 'db_index': 'True'})
        },
        u'paloma.systemevents': {
            'Meta': {'object_name': 'Systemevents', 'db_table': "u'SystemEvents'"},
            'currusage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'CurrUsage'", 'blank': 'True'}),
            'customerid': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'db_column': "u'CustomerID'", 'blank': 'True'}),
            'devicereportedtime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_column': "u'DeviceReportedTime'", 'blank': 'True'}),
            'eventbinarydata': ('django.db.models.fields.TextField', [], {'db_column': "u'EventBinaryData'", 'blank': 'True'}),
            'eventcategory': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'EventCategory'", 'blank': 'True'}),
            'eventid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'EventID'", 'blank': 'True'}),
            'eventlogtype': ('django.db.models.fields.CharField', [], {'max_length': '60L', 'db_column': "u'EventLogType'", 'blank': 'True'}),
            'eventsource': ('django.db.models.fields.CharField', [], {'max_length': '60L', 'db_column': "u'EventSource'", 'blank': 'True'}),
            'eventuser': ('django.db.models.fields.CharField', [], {'max_length': '60L', 'db_column': "u'EventUser'", 'blank': 'True'}),
            'facility': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'Facility'", 'blank': 'True'}),
            'fromhost': ('django.db.models.fields.CharField', [], {'max_length': '60L', 'db_column': "u'FromHost'", 'blank': 'True'}),
            'genericfilename': ('django.db.models.fields.CharField', [], {'max_length': '60L', 'db_column': "u'GenericFileName'", 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "u'ID'"}),
            'importance': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'Importance'", 'blank': 'True'}),
            'infounitid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'InfoUnitID'", 'blank': 'True'}),
            'maxavailable': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'MaxAvailable'", 'blank': 'True'}),
            'maxusage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'MaxUsage'", 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'db_column': "u'Message'", 'blank': 'True'}),
            'minusage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'MinUsage'", 'blank': 'True'}),
            'ntseverity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'NTSeverity'", 'blank': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'Priority'", 'blank': 'True'}),
            'receivedat': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_column': "u'ReceivedAt'", 'blank': 'True'}),
            'syslogtag': ('django.db.models.fields.CharField', [], {'max_length': '60L', 'db_column': "u'SysLogTag'", 'blank': 'True'}),
            'systemid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'SystemID'", 'blank': 'True'})
        },
        u'paloma.systemeventsproperties': {
            'Meta': {'object_name': 'Systemeventsproperties', 'db_table': "u'SystemEventsProperties'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "u'ID'"}),
            'paramname': ('django.db.models.fields.CharField', [], {'max_length': '255L', 'db_column': "u'ParamName'", 'blank': 'True'}),
            'paramvalue': ('django.db.models.fields.TextField', [], {'db_column': "u'ParamValue'", 'blank': 'True'}),
            'systemeventid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'SystemEventID'", 'blank': 'True'})
        },
        u'paloma.targetting': {
            'Meta': {'object_name': 'Targetting'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mediator_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mediator'", 'to': u"orm['contenttypes.ContentType']"}),
            'mediator_object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['paloma.Site']"}),
            'targetter_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'targetter'", 'to': u"orm['contenttypes.ContentType']"}),
            'targetter_object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'paloma.template': {
            'Meta': {'unique_together': "(('site', 'name'),)", 'object_name': 'Template'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['paloma.Site']"}),
            'subject': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'text': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '100'})
        }
    }

    complete_apps = ['paloma']
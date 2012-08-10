# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Notification'
        db.create_table('notifications_notification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Profile'])),
            ('marked_for_removal', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ntype', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('wink', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Wink'], null=True)),
            ('sexytime', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['matchmaker.SexyTime'], null=True)),
            ('match', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['matchmaker.Match'], null=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal('notifications', ['Notification'])


    def backwards(self, orm):
        # Deleting model 'Notification'
        db.delete_table('notifications_notification')


    models = {
        'matchmaker.match': {
            'Meta': {'object_name': 'Match'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matchmaker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matchmaker'", 'to': "orm['users.Profile']"}),
            'p1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prospect1'", 'to': "orm['users.Profile']"}),
            'p1_response': ('django.db.models.fields.CharField', [], {'default': "'Pending'", 'max_length': '10'}),
            'p2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prospect2'", 'to': "orm['users.Profile']"}),
            'p2_response': ('django.db.models.fields.CharField', [], {'default': "'Pending'", 'max_length': '10'}),
            'rejected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})
        },
        'matchmaker.sexytime': {
            'Meta': {'object_name': 'SexyTime'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['matchmaker.Match']", 'null': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'p1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'date1'", 'to': "orm['users.Profile']"}),
            'p1_attending': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'p1_responded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'p2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'date2'", 'to': "orm['users.Profile']"}),
            'p2_attending': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'p2_responded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'when': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'where': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'})
        },
        'notifications.notification': {
            'Meta': {'object_name': 'Notification'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marked_for_removal': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['matchmaker.Match']", 'null': 'True'}),
            'ntype': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Profile']"}),
            'sexytime': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['matchmaker.SexyTime']", 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'wink': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Wink']", 'null': 'True'})
        },
        'users.profile': {
            'Meta': {'object_name': 'Profile'},
            'age': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'banned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'fb_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'fb_link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'fb_profile_pic': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'fb_username': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'profile': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'users.wink': {
            'Meta': {'object_name': 'Wink'},
            'from_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wink_from'", 'to': "orm['users.Profile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'received': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'to_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wink_to'", 'to': "orm['users.Profile']"})
        }
    }

    complete_apps = ['notifications']
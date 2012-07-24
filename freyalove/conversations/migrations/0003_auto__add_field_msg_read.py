# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Msg.read'
        db.add_column('conversations_msg', 'read',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Msg.read'
        db.delete_column('conversations_msg', 'read')


    models = {
        'conversations.conversation': {
            'Meta': {'object_name': 'Conversation'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner_set'", 'to': "orm['users.Profile']"}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'participant_set'", 'to': "orm['users.Profile']"})
        },
        'conversations.msg': {
            'Meta': {'object_name': 'Msg'},
            'conversation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conversations.Conversation']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'receiver_set'", 'to': "orm['users.Profile']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sender_set'", 'to': "orm['users.Profile']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})
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
        }
    }

    complete_apps = ['conversations']
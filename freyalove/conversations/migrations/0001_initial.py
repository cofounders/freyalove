# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Conversation'
        db.create_table('conversations_conversation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='owner_set', to=orm['users.Profile'])),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='participant_set', to=orm['users.Profile'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal('conversations', ['Conversation'])

        # Adding model 'Msg'
        db.create_table('conversations_msg', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sender_set', to=orm['users.Profile'])),
            ('receiver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='receiver_set', to=orm['users.Profile'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal('conversations', ['Msg'])


    def backwards(self, orm):
        # Deleting model 'Conversation'
        db.delete_table('conversations_conversation')

        # Deleting model 'Msg'
        db.delete_table('conversations_msg')


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
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
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